from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal

# Create your models here.

RATING_CHOICES = [
        (Decimal('0.0'), '0.0 stars'),
        (Decimal('0.5'), '0.5 stars'),
        (Decimal('1.0'), '1.0 stars'),
        (Decimal('1.5'), '1.5 stars'),
        (Decimal('2.0'), '2.0 stars'),
        (Decimal('2.5'), '2.5 stars'),
        (Decimal('3.0'), '3.0 stars'),
        (Decimal('3.5'), '3.5 stars'),
        (Decimal('4.0'), '4.0 stars'),
        (Decimal('4.5'), '4.5 stars'),
        (Decimal('5.0'), '5.0 stars'),
    ]


class Author(models.Model):
    """
    Represents an author of a book.

    Fields:
        - name: The name of the author (max length: 200 characters).

    Methods:
        - __str__: Returns the name of the author as a string.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    """
    Represents a book in the system.

    Fields:
        - title: The title of the book (max length: 200 characters).
        - authors: A many-to-many relationship with the Author model.

    Methods:
        - __str__: Returns the book title and its authors as a string.
    """
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        authors = ", ".join(author.name for author in self.authors.all())
        return f"{self.title} by {authors}"


class Review(models.Model):
    """
    Represents a review for a book written by a user.

    Fields:
        - reviewer: A foreign key to the User model, representing the user who
          wrote the review.
        - book: A foreign key to the Book model, representing the book being
          reviewed.
        - content: The full content of the review (max length: 2000
          characters).
        - content_preview: A preview of the review content (first 200
          characters).
        - rating: The rating given to the book, chosen from predefined
          RATING_CHOICES.
        - created_on: The timestamp when the review was created.
        - updated_on: The timestamp when the review was last updated.

    Meta:
        - ordering: Orders reviews by the most recently updated.
        - constraints: Ensures that a user can only write one review per book.

    Methods:
        - save: Automatically generates a content preview when saving the
          review.
        - __str__: Returns a string representation of the review, including the
          book and reviewer.
    """
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reviews"
        )
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    content = models.TextField(max_length=2000)
    content_preview = models.TextField(max_length=200, blank=True, null=True)

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=RATING_CHOICES,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_on']
        constraints = [
            models.UniqueConstraint(
                fields=['reviewer', 'book'],
                name='unique_user_review_for_book'
            )
        ]

    def save(self, *args, **kwargs):
        self.content_preview = self.content[:200]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book} Review | written by {self.reviewer}"
