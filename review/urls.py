from django.urls import path
from review import views as review_views

urlpatterns = [
    path(
        'my-reviews/edit/<int:pk>/', review_views.edit_review,
        name='edit_review'
    ),
    path(
        'my-reviews/delete/<int:pk>/', review_views.delete_review,
        name='delete_review'
    ),
    path('my-reviews/', review_views.UserReviewList.as_view(),
         name='user_review_list'),
    path('add-review/', review_views.add_review, name='add_review'),
    path('<int:pk>/', review_views.review_detail, name='review_detail'),
    path('', review_views.AllReviewList.as_view(), name='index'),
]
