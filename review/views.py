from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Min
from django.forms import HiddenInput
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Review, Author, Book
from .forms import ReviewForm

# Create your views here.


class AllReviewList(generic.ListView):
    """
    View to display a paginated list of all reviews.

    - Fetches all reviews from the database.
    - Annotates the queryset with the first author's name for sorting.
    - Supports sorting by book title, author name, or last updated date.

    Template:
        - review/index.html

    Pagination:
        - 12 reviews per page.

    Methods:
        - get_queryset: Fetches reviews and related fields.
        - get_ordering: Determines the ordering of the reviews based on
          the 'sort' query parameter.
    """

    template_name = "review/index.html"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Review.objects.all()
            .select_related('book')
            .prefetch_related('book__authors')
        )
        queryset = queryset.annotate(
            first_author=Min('book__authors__name'))

        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-updated_on')
        return queryset

    def get_ordering(self):
        sort_option = self.request.GET.get('sort', '-updated_on')
        if sort_option == 'book':
            return 'book__title'
        elif sort_option == 'author':
            return 'first_author'
        return sort_option


class UserReviewList(LoginRequiredMixin, generic.ListView):

    class UserReviewList(LoginRequiredMixin, generic.ListView):
        """
        View to display a paginated list of reviews submitted by the logged-in 
        user.

        - Fetches reviews created by the currently logged-in user.
        - Annotates the queryset with the first author's name for sorting.
        - Supports sorting by book title, author name, or last updated date.

        Template:
            - review/user_review_list.html

        Pagination:
            - 12 reviews per page.

        Methods:
            - get_queryset: Fetches reviews and related fields.
            - get_ordering: Determines the ordering of the reviews based on
            the 'sort' query parameter.
        """

    template_name = "review/user_review_list.html"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Review.objects.filter(reviewer=self.request.user)
            .select_related('book')
            .prefetch_related('book__authors')
        )
        queryset = queryset.annotate(
            first_author=Min('book__authors__name'))

        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-updated_on')
        return queryset

    def get_ordering(self):
        sort_option = self.request.GET.get('sort', '-updated_on')
        if sort_option == 'book':
            return 'book__title'
        elif sort_option == 'author':
            return 'first_author'
        return sort_option


def review_detail(request, pk):
    """
    View to display the details of a specific review.

    - Fetches the review with the given primary key.
    - Determines if the logged-in user is the owner of the review.

    Template:
        - review/review_detail.html

    Context:
        - review: The review object to display.
        - is_own_review: Boolean indicating if the review belongs to the
          logged-in user.
    """

    queryset = (
        Review.objects.all()
        .select_related('book')
        .prefetch_related('book__authors')
    )
    review = get_object_or_404(queryset, pk=pk)
    is_own_review = False
    if review.reviewer == request.user:
        is_own_review = True
    return render(
        request,
        'review/review_detail.html',
        {'review': review,
         'is_own_review': is_own_review}
    )


@login_required
def add_review(request):
    """
    View to add a new review.

    Features:
        - Handles form submission for creating a new review.
        - Processes the 'authors' field to create or retrieve Author objects.
        - Creates or retrieves a Book object based on the title and associated
          authors.
        - Associates the review with the logged-in user and the book.
        - Prevents duplicate reviews for the same book by the same user.

    Template:
        - review/add_review.html

    Context:
        - review_form: The form for adding a new review.

    Messages:
        - Success: Displays a success message when the review is added.
        - Error: Displays an error message if the user tries to add a duplicate
          review for the same book.
    """
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            # cleans author names, splits - each is then
            # retrieved or created as an author object, list is used to set
            # relationship with book
            author_names = review_form.cleaned_data['authors'].split(',')
            authors = []
            for name in author_names:
                name = name.strip().title()
                author, created = Author.objects.get_or_create(name=name)
                authors.append(author)

            book_title = review_form.cleaned_data['book'].strip().title()
            # if book with those authors already exists, use that book object
            # if not, create it and set authors
            book = None
            books_with_same_title = Book.objects.filter(title=book_title)
            for existing_book in books_with_same_title:
                # convert to sets so list and queryset can be compared
                if set(existing_book.authors.all()) == set(authors):
                    book = existing_book
                    break
            if not book:
                book = book = Book.objects.create(title=book_title)
                book.authors.set(authors)
            # add reviewer, associate book and authors with review
            review = review_form.save(commit=False)
            review.reviewer = request.user
            review.book = book
            try:
                review.save()
                messages.add_message(request, messages.SUCCESS,
                                     'You have added a new review!')
            except IntegrityError:
                review_form.add_error(
                    None,
                    ("You have already created a review for this book. "
                     "Please edit your previous review instead of adding a"
                     " new one.")
                )
                messages.add_message(
                    request,
                    messages.ERROR,
                    (
                        'You cannot have multiple reviews for the same book. '
                        'Please edit your previous review.'
                    )
                )
            else:
                return redirect('user_review_list')

    else:
        review_form = ReviewForm()

    return render(
        request,
        'review/add_review.html',
        {'review_form': review_form}
    )


@login_required
def edit_review(request, pk):
    """
    View to edit an existing review.

    - Fetches the review with the given primary key for editing.
    - Ensures that only the owner of the review can edit it.
    - Handles form submission for updating the review.
    - Prevents duplicate reviews for the same book by the same user.

    Template:
        - Uses the "review/edit_review.html" template.

    Context:
        - review_form: The form for editing the review.
        - review: The review object being edited.

    Messages:
        - Success: Displays a success message when the review is updated.
        - Warning: Displays a warning message if there are validation errors
          or if the user tries to edit a review they do not own.
    """
    review = get_object_or_404(Review, pk=pk)

    if review.reviewer != request.user:
        messages.add_message(
            request, messages.WARNING,
            'You can only edit your own reviews.'
        )
        return redirect('review_detail', pk=review.pk)

    if request.method == "POST":
        review_form = ReviewForm(data=request.POST, instance=review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            try:
                review.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    'You have edited your review.'
                )
            except ValidationError as e:
                review_form.add_error(None, (str(e)))
                messages.add_message(
                    request,
                    messages.WARNING,
                    (
                        'There was an error saving your review. '
                        'Please fix the issues below.'
                    )
                )

        return redirect('review_detail', pk=review.pk)

    else:
        review_form = ReviewForm(instance=review)
        review_form.fields['book'].initial = review.book.title
        review_form.fields['authors'].initial = ", ".join(
            [author.name for author in review.book.authors.all()]
        )
        review_form.fields['book'].widget = HiddenInput()
        review_form.fields['authors'].widget = HiddenInput()

    return render(
        request,
        'review/edit_review.html',
        {'review_form': review_form, 'review': review}
    )


@login_required
def delete_review(request, pk):
    """
    View to delete an existing review.

    - Fetches the review with the given primary key (pk) for deletion.
    - Ensures that only the owner of the review can delete it.
    - Deletes the review from the database.

    Redirects:
        - Redirects to the review detail page if the user does not own the
          review.
        - Redirects to the user's review list after successful deletion.

    Messages:
        - Success: Displays a success message when the review is deleted.
        - Warning: Displays a warning message if the user tries to delete a
          review they do not own.
    """
    review = get_object_or_404(Review, pk=pk)

    if review.reviewer != request.user:
        messages.add_message(request, messages.WARNING,
                             'You can only delete your own reviews.')
        return redirect('review_detail', pk=review.pk)

    review.delete()
    messages.add_message(request, messages.SUCCESS,
                         'You have deleted your review.')
    return redirect('user_review_list')
