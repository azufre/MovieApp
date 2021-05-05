from django.urls import path
from . import views

urlpatterns = [
    path('movie/', views.MovieList.as_view()),
    path('movie/detail/<int:pk>', views.MovieDetail.as_view()),
    path('ratereview/', views.RateReviewList.as_view()),
    path('ratereview/detail/', views.RateReviewDetail.as_view()),
]