from django.urls import path
from review import views as review_views

urlpatterns = [
    path('<int:pk>', review_views.review_detail, name='review_detail'),
    path('my-reviews/', review_views.UserReviewList.as_view(), name='user_review_list'),
    path('', review_views.AllReviewList.as_view(), name='index'),
]
