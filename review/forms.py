from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """
    A form for creating and editing reviews.

    Fields:
        - authors: A CharField for entering one or more authors,
          separated by commas (author objects created in view).
        - book: A CharField for entering the book title (book objects created
          in view).
        - content: A TextField for the review content (from the Review model).
        - rating: A field for the book rating (from the Review model).

    Custom Validation:
        - clean_authors: Ensures that multiple authors are separated by commas.
    """
    authors = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter author(s), separated by commas',
            'required': True
        })
    )
    book = forms.CharField(widget=forms.TextInput(attrs={
                'placeholder': 'Enter book title',
                'required': True
            }),
    )

    def clean_authors(self):
        authors = self.cleaned_data.get('authors', '').strip()
        # Allow single author or comma-separated authors
        if ',' not in authors and len(authors.split()) > 2:
            raise forms.ValidationError(
                "Please separate multiple authors with commas."
            )
        return authors

    class Meta:
        model = Review
        fields = ('content', 'rating',)

    field_order = ['book', 'authors', 'content', 'rating']
