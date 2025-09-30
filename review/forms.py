from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    authors = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter author(s), separated by commas',
            'required': True
        })
    )

    class Meta:
        model = Review
        fields = ('book', 'content', 'rating',)
        widgets = {
            'book': forms.TextInput(attrs={
                'placeholder': 'Enter book title',
                'required': True
            }),
        }
