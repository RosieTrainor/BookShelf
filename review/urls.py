from django.urls import path
from review import views as review_views

urlpatterns = [
    path('', review_views.AllReviewList.as_view(), name='index'),
    path('my-reviews/', review_views.UserReviewList.as_view(), name='user_review_list'),
]
