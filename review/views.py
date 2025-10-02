from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
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

    queryset = Review.objects.all()
    template_name = "review/index.html"
    paginate_by = 6


class UserReviewList(LoginRequiredMixin, generic.ListView):

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

    template_name = "review/user_review_list.html"
    paginate_by = 6


def review_detail(request, pk):

    queryset = Review.objects.all()
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
    view to a delete a review
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
