from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review

# Create your views here.


class ReviewList(LoginRequiredMixin, generic.ListView):

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)
    
    template_name = "review/review_list.html"
    paginate_by = 6
