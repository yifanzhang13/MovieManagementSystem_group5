from django.shortcuts import render
from .models import Movies, Users, Ratings, Links, Tags
from django.db import connection
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from library.forms import SearchMovieForm
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
        results = cursor.fetchall()
    finally:
        cursor.close()  
    all = []
    for row in results:
        dic = {
            'MovieID':row[0],
            'MovieTitle':row[1],
            'MovieGenres':row[2],
        }
        all.append(dic)
    context = {
        'movies':all,
    }
    return render(request, 'Movies.html', context=context)

class MovieDetailView(generic.DetailView):
    model = Movies

def MovieDetail(request, pk):
    movie = get_object_or_404(Movies, pk=pk)
    print(pk)
    cursor = connection.cursor()
    try:
        movie = cursor.execute('SELECT * FROM library_movies WHERE MovieID = '+str(pk))
        results = cursor.fetchall()
        print(results)
    finally:
        cursor.close()  
    all = []
    for row in results:
        dic = {
            'MovieID':row[0],
            'MovieTitle':row[1],
            'MovieGenres':row[2],
        }
        all.append(dic)
    context = {
        'movies':all,
    }

    return render(request, 'library/movies_detail.html', context=context)

# def MovieDetail(request, pk):
#     movie = get_object_or_404(Movies, pk=pk)
#     print(pk) # pk等于14 http://127.0.0.1:8000/library/movies/14

#     # form = SearchMovieForm()
#     # if request.method == 'POST':
#     #     form = SearchMovieForm(request.POST)
#     #     if form.is_valid():
#     #         return HttpResponseRedirect('http://127.0.0.1:8000/library/movies/'+str(2))

#     context = {
#         'movie': movie,
#     }

#     return render(request, 'library/movies_detail.html', context)

class MoviesListView(generic.ListView):
    # The generic view will query the database to get all records for the specified model 
    # (Movies) then render a template located 
    # at /locallibrary/catalog/templates/catalog/Movies_list.html (which we will create below). 
    # Within the template you can access the list of books with the 
    # template variable named object_list OR book_list (i.e. generically "the_model_name_list").
    model = Movies