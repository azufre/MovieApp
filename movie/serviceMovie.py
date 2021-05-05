from .models import Movie, RateReview
from django.db.models import Sum

class ServiceMovie:

    def setRate(self, rateReview: RateReview):

        totalRates = RateReview.objects.filter(movie__pk=rateReview.movie.pk).count()
        totalStars = RateReview.objects.filter(movie__pk=rateReview.movie.pk).aggregate(total=Sum('stars'))['total'] or 0
        audience_score = 0
 
        if totalStars > 0:
            audience_score = ((totalStars * 20)  / totalRates)

        rateReview.movie.audience_score = audience_score
        rateReview.movie.save()
