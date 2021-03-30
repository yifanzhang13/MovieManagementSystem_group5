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
    form = SearchMovieForm()
    if request.method == 'POST':
        form = SearchMovieForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('http://127.0.0.1:8000/library/movies/'+str(2))
    
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

def search(request):
    context = {}
    return render(request, "library/search.html", context=context)

def handle(request):
    text = request.POST["search_content"] # user input text
    movie_report = {}
    po_list = []
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM library_movies')
        results = cursor.fetchall()
        for row in results:
        # id title genres
            if text == row[1]: # 可以找到准确的电影
                movie_report['MovieTitle'] = row[1]
                movie_report['MovieID'] = row[0]
                movie_report['MovieGenres'] = str(row[2]).replace("|"," & ")
                movie_report['test'] = 'test11'
            if text in row[1]: # 只能找到带有用户搜索关键字的电影
                # js不支持tuple
                dic = {
                    'MovieID':row[0],
                    'MovieTitle':row[1],
                    'MovieGenres':row[2],
                }
                po_list.append(dic)
        if movie_report:
            # 看过这个电影并打过分的人数
            cursor.execute('SELECT count(*) FROM library_ratings WHERE MovieID_id = %s', [movie_report['MovieID']])
            results = cursor.fetchall()
            for row in results:
                movie_report['number_of_ratings'] = row[0]
            # 电影的平均分
            cursor.execute('SELECT RatingScore FROM library_ratings WHERE MovieID_id = %s', [movie_report['MovieID']])
            results = cursor.fetchall()
            print(results)
            total_rating_score = 0
            for row in results:
                total_rating_score += row[0]
            print(total_rating_score)
            movie_report['average_rating_score'] = round(float(total_rating_score/movie_report['number_of_ratings']),2)
            # 电影tags
            cursor.execute('SELECT TagContent FROM library_tags WHERE MovieID_id = %s', [movie_report['MovieID']])
            results = cursor.fetchall()
            print(results)
            total_tag = ''
            for row in results:
                total_tag =  row[0] + ', ' + total_tag
            print(total_tag)
    finally:
        cursor.close()
    context = {
        'resp':po_list,
        'report':movie_report,
    }
    return render(request, "library/resp.html", context=context)

def handle_backup(request):
    text = request.POST["search_content"] # user input text
    db = Movies.objects.all()
    movie_report = []
    po_list = []
    for i in db:
        if text == i.MovieTitle:
            movie_report = i

        if text in i.MovieTitle:
            po_list.append(i)
    context = {
        'resp':po_list,
        'report':movie_report,
    }

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