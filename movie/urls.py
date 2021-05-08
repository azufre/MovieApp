from django.urls import path
from . import views

urlpatterns = [
    path('movie/list/', views.MovieList.as_view(), name='movieList'),
    path('movie/create/', views.MovieCreate.as_view(), name='movieCreate'),
    path('movie/view/<int:pk>/', views.MovieViewSet.as_view(), name='movieView'),
    path('movie/detail/<int:pk>/', views.MovieDetail.as_view(), name='movieDetail'),
    path('ratereview/list/', views.RateReviewList.as_view(), name='ratereViewList'),
    path('ratereview/create/', views.RateReviewCreate.as_view(), name="ratereViewCreate"),
]