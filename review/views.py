from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review

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
