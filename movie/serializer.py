from rest_framework import serializers
from .models import Movie, RateReview

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'pk',
            'title', 
            'year',
            'rated', 
            'released_on',
            'genre',
            'director',
            'plot',
            'audience_score',
            'created_at',
            'updated_at'
        ]

        extra_kwargs = {
            'created_at': {'required': False},
            'updated_at': {'required': False},
            'owner': {'required': False},
            'audience_score': {'required': False},
        }

class RateReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = RateReview
        fields = [
            'pk',
            'movie', 
            'stars', 
            'rewiew', 
            'created_at', 
            'updated_at',
            'owner',
        ]

        extra_kwargs = {
            'created_at': {'required': False},
            'updated_at': {'required': False},
            'owner': {'required': False},
        }