from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
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