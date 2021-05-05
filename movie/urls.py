from django.urls import path
from . import views

urlpatterns = [
    path('movie/', views.MovieList.as_view(), name='movie'),
    path('movie/detail/<int:pk>', views.MovieDetail.as_view(), name='movieDetail'),
    path('ratereview/', views.RateReviewList.as_view(), name='ratereview'),
    path('ratereview/detail/', views.RateReviewDetail.as_view(), name="ratereviewDetail"),
]