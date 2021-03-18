from django.shortcuts import render
from .models import Movies, Users, Ratings, Links, Tags
# Create your views here.

def index(request):
    # Generate counts of movies
    num_movies = Movies.objects.all().count()
    