from django.urls import path
from review import views as review_views

urlpatterns = [
    path('', review_views.index, name='index'),
]
