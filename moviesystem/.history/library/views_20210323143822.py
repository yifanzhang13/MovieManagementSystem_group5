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

def MoviesView(request):
    cursor = connection.cursor()
    try:
        movies = cursor.execute('SELECT * FROM library_movies')
    finally:
        cursor.close()
    
    all = []
    for movie in movies:
        dic = {
            'MovieID':movie.MovieID,
            'MovieTitle':movie.MovieTitle,
            'MovieGenres':movie.MovieGenres,
        }
        all.append(dic)
    
    context = {
        'books':all,
    }

    # 所有的movie
    # movies = Movies.objects.all()
    # context = {
    #     'movies':movies,
    # }
    return render(request, 'Movies.html', context=context)


class MoviesListView(generic.ListView):
    # The generic view will query the database to get all records for the specified model 
    # (Movies) then render a template located 
    # at /locallibrary/catalog/templates/catalog/Movies_list.html (which we will create below). 
    # Within the template you can access the list of books with the 
    # template variable named object_list OR book_list (i.e. generically "the_model_name_list").
    model = Movies