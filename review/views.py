from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
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
            # cleans book names - retrieved or created book object
            book_title = review_form.cleaned_data['book'].strip().title()
            book, created = Book.objects.get_or_create(title=book_title)
            # add reviewer, associate book and authors with review
            review = review_form.save(commit=False)
            review.reviewer = request.user
            review.book = book
            review.book.authors.set(authors)
            try:
                review.save()
            except IntegrityError:
                review_form.add_error(
                    None,
                    ("You have already created a review for this book. "
                     "Please edit your previous review instead of adding a"
                     " new one.")
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
