from django.shortcuts import render
from .models import Movies, Users, Ratings, Links, Tags
from django.db import connection
from django.views import generic
# Create your views here.

def index(request):
    cursor = connection.cursor()
    try:
        num_movies = cursor.execute('SELECT * FROM library_movies')
        rating_5 = cursor.execute('SELECT * FROM library_ratings WHERE RatingScore = 5')
        rating_4 = cursor.execute('SELECT * FROM library_ratings WHERE RatingScore = 4')
        rating_3 = cursor.execute('SELECT * FROM library_ratings WHERE RatingScore = 3')
        rating_2 = cursor.execute('SELECT * FROM library_ratings WHERE RatingScore = 2')
        rating_1 = cursor.execute('SELECT * FROM library_ratings WHERE RatingScore = 1')
    finally:
        cursor.close()

    context = {
        'num_movies':num_movies,
        'rating_5':rating_5,
        'rating_4':rating_4,
        'rating_3':rating_3,
        'rating_2':rating_2,
        'rating_1':rating_1,
    }

    return render(request, 'index.html', context=context)

class MovieListView(generic.ListView):
    # The generic view will query the database to get all records for 
    # the specified model (Book) then render a template located 
    # at /locallibrary/catalog/templates/catalog/book_list.html
    model = Movies