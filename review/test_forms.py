from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import Author, Book, Review
from .forms import ReviewForm

# Create your tests here.


class ReviewFormTests(TestCase):
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(username='testuser1', password='password1')
        self.user2 = User.objects.create_user(username='testuser2', password='password2')

    def test_no_duplicate_book_or_author(self):
        # Create an author and book
        author = Author.objects.create(name="George Orwell")
        book = Book.objects.create(title="1984")
        book.authors.add(author)

        # User 1 submits a review for the book
        Review.objects.create(book=book, reviewer=self.user1, content="Loved it!", rating=5.0)

        # User 2 submits a review for the same book and author
        form_data = {
            'authors': 'George Orwell',
            'book': '1984',
            'content': 'Amazing book!',
            'rating': 4.5,
        }
        form = ReviewForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

        # Save the review
        review = form.save(commit=False)
        review.reviewer = self.user2
        review.save()

        # Check that no duplicate book or author is created
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Review.objects.count(), 2)

    def test_case_insensitivity_author(self):
        # Create an author and book with titlecase
        author = Author.objects.create(name="George Orwell")
        book = Book.objects.create(title="1984")
        book.authors.add(author)

        # Submit a form with different casing
        form_data = {
            'authors': 'george orwell',
            'book': '1984',
            'content': 'Still great!',
            'rating': 4.0,
        }
        form = ReviewForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

        # Check that no duplicate author or book is created
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Book.objects.count(), 1)

    def test_case_insensitivity_book(self):
        # Create an author and book with titlecase
        author = Author.objects.create(name="Jane Austen")
        book = Book.objects.create(title="Emma")
        book.authors.add(author)

        # Submit a form with different casing
        form_data = {
            'authors': 'Jane Austen',
            'book': 'emMa',
            'content': 'Still great!',
            'rating': 4.0,
        }
        form = ReviewForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

        # Check that no duplicate author or book is created
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Book.objects.count(), 1)

    def test_author_associated_with_book(self):
        # Submit a form with a new author and book
        form_data = {
            'authors': 'Aldous Huxley',
            'book': 'Brave New World',
            'content': 'A classic!',
            'rating': 5.0,
        }
        form = ReviewForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

        # Save the review
        review = form.save(commit=False)
        review.reviewer = self.user1
        review.save()

        # Check that the author is associated with the book
        book = Book.objects.get(title="Brave New World")
        self.assertEqual(book.authors.count(), 1)
        self.assertEqual(book.authors.first().name, "Aldous Huxley")

    def test_book_associated_with_review(self):
        # Submit a form with a new book
        form_data = {
            'authors': 'Aldous Huxley',
            'book': 'Brave New World',
            'content': 'A classic!',
            'rating': 5.0,
        }
        form = ReviewForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

        # Save the review
        review = form.save(commit=False)
        review.reviewer = self.user1
        review.save()

        # Check that the review is associated with the book
        self.assertEqual(review.book.title, "Brave New World")

    def test_reviewer_has_one_review_per_book(self):
        # Create an author and book
        author = Author.objects.create(name="George Orwell")
        book = Book.objects.create(title="1984")
        book.authors.add(author)

        # Create a review for the book
        Review.objects.create(book=book, reviewer=self.user1, content="Good", rating=3.5)

        # Submit a form for the same book and user
        form_data = {
            'authors': 'George Orwell',
            'book': '1984',
            'content': 'Still amazing!',
            'rating': 4.0,
        }
        form = ReviewForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

        # Save the review and check for duplicates
        with self.assertRaises(IntegrityError):
            review = form.save(commit=False)
            review.reviewer = self.user1
            review.save()

    def test_author_does_not_change_if_same_title_different_author(self):
        # Create a book with one author
        author1 = Author.objects.create(name="George Orwell")
        book1 = Book.objects.create(title="Animal Farm")
        book1.authors.add(author1)

        # Submit a form with the same title but a different author
        form_data = {
            'authors': 'Aldous Huxley',
            'book': 'Animal Farm',
            'content': 'A different perspective!',
            'rating': 4.0,
        }
        form = ReviewForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

        # Save the review
        review = form.save(commit=False)
        review.reviewer = self.user2
        review.save()

        # Check that a new book is created
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Author.objects.count(), 2)

        # Check that each book is associated with the correct author
        book2 = Book.objects.get(title="Animal Farm", authors__name="Aldous Huxley")
        self.assertEqual(book1.authors.first().name, "George Orwell")
        self.assertEqual(book2.authors.first().name, "Aldous Huxley")