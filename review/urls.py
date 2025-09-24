from django.urls import path
from review import views as review_views

urlpatterns = [
    path('', review_views.ReviewList.as_view(), name='user_review_list'),
]
