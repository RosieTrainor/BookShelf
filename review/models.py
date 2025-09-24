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
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Author: {self.name}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        authors = ", ".join(author.name for author in self.authors.all())
        return f"{self.title} by {authors}"


class Review(models.Model):
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reviews"
        )
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    content = models.TextField(max_length=2000)
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

    def __str__(self):
        return f"{self.book} Review | written by {self.reviewer}"
