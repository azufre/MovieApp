from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serializer import MovieSerializer, RateReviewSerializer
from .models import Movie, RateReview
from .serviceMovie import ServiceMovie

# Create your views here.
class MovieList(generics.ListAPIView):

    """
    List all the Movies and create movie
    """
    serializer_class =  MovieSerializer

    def get_queryset(self):

        queryset = Movie.objects.all().order_by('-created_at', '-audience_score')

        query_title = self.request.query_params.get('title')

        if query_title is not None:
            queryset = queryset.filter(title__icontains=query_title)    

        return queryset

class MovieCreate(APIView):

    serializer_class =  MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            serializer.save(owner = self.request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieViewSet(APIView):

    serializer_class =  MovieSerializer

    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer = self.serializer_class(movie)
        return Response(serializer.data)

class MovieDetail(APIView):

    """
    Update, get and delete movie
    """

    serializer_class =  MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer = self.serializer_class(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def delete(self, request, pk, format=None):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RateReviewList(generics.ListAPIView):

    """
    List all the RateReviews and create ratereview
    """

    serializer_class =  RateReviewSerializer

    def get_queryset(self):

        queryset = RateReview.objects.all().order_by('-created_at')

        query_id_movie = self.request.query_params.get('idmovie', None)
        
        if query_id_movie is not None:

            try:

                query_id_movie = int(query_id_movie)

            except:
                query_id_movie = 0    

            queryset = queryset.filter(movie__pk=query_id_movie)    

        return queryset

class RateReviewCreate(APIView):

    def __init__(self):
        self._serviceMovie = ServiceMovie()

    serializer_class =  RateReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    custom_error = {
        'movie': ['Already exist a review for this movie with the current user logged']
    }

    def put(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            checkIfAlreadyExistReview = RateReview.objects.filter(owner__pk=request.user.pk, movie__pk=serializer.validated_data['movie'].pk).exists()

            if checkIfAlreadyExistReview:
                return Response(self.custom_error, status=status.HTTP_400_BAD_REQUEST)

            instance = serializer.save(owner = self.request.user)
            self._serviceMovie.setRate(instance)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
