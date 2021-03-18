from django.shortcuts import render
from .models import Movies, Users, Ratings, Links, Tags
# Create your views here.

def index(request):
    # Generate counts of movies
    num_movies = Movies.objects.all().count()
    # number of different ratingscore movies
    rating_5 = Ratings.objects.filter(RatingScore__exact='5').count()
    rating_4 = Ratings.objects.filter(RatingScore__exact='4').count()
    rating_3 = Ratings.objects.filter(RatingScore__exact='3').count()
    rating_2 = Ratings.objects.filter(RatingScore__exact='2').count()
    rating_1 = Ratings.objects.filter(RatingScore__exact='1').count()

    context = {
        'num_movies':num_movies,
        'rating_5':rating_5,
        'rating_4':rating_4,
        'rating_3':rating_3,
        'rating_2':rating_2,
        'rating_1':rating_1,
    }

    return render(request, 'index.html', context=context)