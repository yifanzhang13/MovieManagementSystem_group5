from django.shortcuts import render
from .models import Movies, Users, Ratings, Links, Tags
from django.db import connection
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from library.forms import SearchMovieForm
import numpy as np
import pandas as pd
import library.recommend_service as recommend_service
import re
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
        sql = '''
                SELECT DISTINCT m.MovieID, m.MovieTitle, m.MovieGenres
                FROM library_movies AS m, library_links AS l
                WHERE m.MovieID = l.MovieID_id
                ORDER BY m.MovieID ASC
            '''
        cursor.execute(sql)
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
        'movie_title': 'Movies List'
    }
    return render(request, 'Movies.html', context=context)

def AlphabetSortedMoviesView(request):
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM library_movies AS m ORDER BY m.MovieTitle')
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
        'movie_title': 'Movies List'
    }
    return render(request, 'sorted_movies.html', context=context)

def ReverseAlphabetSortedMoviesView(request):
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM library_movies AS m ORDER BY m.MovieTitle DESC')
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
        'movie_title': 'Movies List'
    }
    return render(request, 'sorted_movies.html', context=context)

def RatingNumSortedMoviesView(request):
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM library_movies AS m ORDER BY m.MovieTitle')
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
        'movie_title': 'Movies List'
    }
    return render(request, 'sorted_movies.html', context=context)


def PopularMoviesView(request):
    cursor = connection.cursor()
    try:
        sql = '''
            SELECT DISTINCT m.MovieID, m.MovieTitle, m.MovieGenres
            FROM library_movies AS m
            WHERE MovieID IN (SELECT MovieID_id 
            FROM library_ratings 
            GROUP BY MovieID_id 
            HAVING AVG(RatingScore) >= 4 AND COUNT(RatingScore)>=100)
            ORDER BY m.MovieTitle ASC
            LIMIT 100
        '''
        cursor.execute(sql)
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
        'movie_title': 'Popular Movies List'
    }
    return render(request, 'popularmovies.html', context=context)


def PolarisingMoviesView(request):
    cursor = connection.cursor()
    try:
        sql = '''
            SELECT DISTINCT r.MovieID_id 
            FROM library_ratings AS r
            GROUP BY r.MovieID_id 
            HAVING COUNT(MovieID_id)>=10 
            ORDER BY STDDEV(RatingScore) DESC 
            LIMIT 20
        '''
        cursor.execute(sql)
        results = cursor.fetchall()
        movieID=[row[0] for row in results]
        sql = "SELECT * FROM library_movies where MovieID in {0}".format(tuple(movieID))
        cursor.execute(sql)
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
        'movie_title': 'Polarising Movies List'
    }
    return render(request, 'popularmovies.html', context=context)

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
    sql_findtags = '''
                SELECT m.MovieID, SUBSTR(MovieTitle, INSTR(MovieTitle,"(") + 1, 
                INSTR(MovieTitle,")") - INSTR(MovieTitle,"(") - 1) AS extracted,
                SUBSTRING_INDEX(SUBSTRING_INDEX(m.MovieGenres,'|',b.help_topic_id+1),'|',-1) AS genres
                FROM library_movies AS m
                JOIN
                mysql.help_topic b
                ON b.help_topic_id < (LENGTH(m.MovieGenres) - LENGTH(REPLACE(m.MovieGenres,'|',''))+1)
                ORDER BY m.MovieID;
    '''
    text = request.POST["search_content"] # user input text
    movie_report = {}
    po_list = []
    cursor = connection.cursor()
    try:
        sql = '''
                SELECT DISTINCT m.MovieID, m.MovieTitle, m.MovieGenres
                FROM library_movies AS m, library_links AS l
                WHERE m.MovieID = l.MovieID_id
                ORDER BY m.MovieID ASC
            '''
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
        # id title genres
            if text == row[1]:
                # find movie name
                name = str(row[1])
                ind = name.index('(') # find the index of the first ( in the name
                movie_report['MovieTitle'] = name[0:ind] # ignore the alias and release year in the title to find the name of the movie

                # find movie released year and alias
                title = str(row[1])
                p1 = re.compile(r'[(](.*?)[)]', re.S) # extract strings within ()
                print(re.findall(p1, title))
                list_strings = re.findall(p1, title)
                if len(list_strings) == 1:
                    movie_report['ReleasedYear'] = list_strings[0]
                else:
                    if 'a.k.a.' in list_strings[0]:
                        movie_report['MovieAlias'] = list_strings[0].replace('a.k.a.','') # delete a.k.a.
                        movie_report['ReleasedYear'] = list_strings[1]
                    else:
                        movie_report['ReleasedYear'] = list_strings[1]
                        movie_report['MovieAlias'] = list_strings[0]

                movie_report['MovieID'] = row[0]
                movie_report['MovieGenres'] = str(row[2]).replace("|"," & ")
            if text in row[1]:
                dic = {
                    'MovieID':row[0],
                    'MovieTitle':row[1],
                    'MovieGenres':str(row[2]).replace("|"," & "),
                }
                po_list.append(dic)

        if movie_report:
            # number of ratings
            sql = '''
                    SELECT COUNT(*), ROUND(AVG(r.RatingScore), 2) 
                    FROM library_ratings AS r
                    WHERE MovieID_id = %s
                    GROUP BY r.RatingScore WITH ROLLUP
                    LIMIT 6
                '''
            cursor.execute(sql, [movie_report['MovieID']])
            results = cursor.fetchall()
            movie_report['rating_5'] = 0 # initiate to 0 because some movies have no users rated it as 5 or 4 or 3 ...etc
            movie_report['rating_4'] = 0
            movie_report['rating_3'] = 0
            movie_report['rating_2'] = 0
            movie_report['rating_1'] = 0
            print('-----')
            print(results)
            for row in results:
                if row[1] == 5.00:
                    print(row[1])
                    movie_report['rating_5'] = row[0]
                elif row[1] == 4.00:
                    print(row[1])
                    movie_report['rating_4'] = row[0]
                elif row[1] == 3.00:
                    print(row[1])
                    movie_report['rating_3'] = row[0]
                elif row[1] == 2.00:
                    print(row[1])
                    movie_report['rating_2'] = row[0]
                elif row[1] == 1.00:
                    print(row[1])
                    movie_report['rating_1'] = row[0]
                else:
                    movie_report['number_of_ratings'] = row[0]
                    movie_report['average_rating_score'] = row[1]
                print(row)
            print('-----')

            # find tags
            sql = '''
                    SELECT DISTINCT t.TagContent, COUNT(*)
                    FROM library_tags AS t
                    WHERE t.MovieID_id = %s
                    GROUP BY t.TagContent
                    ORDER BY t.TagContent ASC
                '''
            cursor.execute(sql, [movie_report['MovieID']])
            results = cursor.fetchall()
            print(results)
            total_tag = []
            for row in results:
                dic = {
                    'tag':row[0],
                }
                total_tag.append(dic)
            print(total_tag)
            movie_report['tags'] = total_tag

            sql = '''
                    SELECT DISTINCT l.imdbID, l.tmdbID
                    FROM library_links AS l
                    WHERE l.MovieID_id = %s
                '''
            cursor.execute(sql, [movie_report['MovieID']])
            results = cursor.fetchall()
            print(results)
            movie_report['imdbID'] = results[0][0]
            movie_report['tmdbID'] = results[0][1]
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

class MoviesListView(generic.ListView):
    # The generic view will query the database to get all records for the specified model 
    # (Movies) then render a template located 
    # at /locallibrary/catalog/templates/catalog/Movies_list.html (which we will create below). 
    # Within the template you can access the list of books with the 
    # template variable named object_list OR book_list (i.e. generically "the_model_name_list").
    model = Movies

def audience_classification(request):
    print("audience classification...")
    cursor = connection.cursor()
    try:
        ratings = cursor.execute('SELECT * FROM library_ratings')
        results = cursor.fetchall()
    finally:
        cursor.close()
    all_ratings = []
    for row in results:
        dic = {
            'UserID': row[4],
            'MovieID': row[3],
            'RatingScore': row[1],
        }
        all_ratings.append(dic)
    # print(all_ratings)
    user_info = {}
    for i in range(len(all_ratings)):
        if all_ratings[i]['UserID'] not in user_info.keys():
            user_info[all_ratings[i]['UserID']] = [all_ratings[i]['RatingScore']]
        else:
            user_info[all_ratings[i]['UserID']].append(all_ratings[i]['RatingScore'])
    ratings_values = []
    for k, v in user_info.items():
        t = np.sum(v) / len(v)
        ratings_values.append(round(t,2))
        if t >= 3.0:
            user_info[k] = "positive"
        else:
            user_info[k] = "negative"
    results = []
    user_info_keys_list = list(user_info.keys())
    user_info_values_list = list(user_info.values())
    for j in range(len(user_info.keys())):
        results.append({
            "userID": user_info_keys_list[j],
            "lable": user_info_values_list[j],
            "ratings_ave": ratings_values[j],
        })

    context = {
        'results': results
    }
    return render(request, 'library/audience_classfication.html', context=context)

def to_predicting_ratings(request):
    return render(request, 'library/predicting_ratings.html')

def to_predicting_personality_traits(request):
    return render(request, 'library/predicting_presonality_traits.html')

def predicting_ratings(request):
    in_userID = request.POST.get("in_userID")
    in_movieID = request.POST.get("in_movieID")
    in_movieName_list = str(in_movieID).split(",")
    print(in_userID)
    print(in_movieName_list)
    cursor = connection.cursor()
    try:
        ratings = cursor.execute('SELECT * FROM library_ratings')
        results = cursor.fetchall()
    finally:
        cursor.close()
    UserID_list = []
    MovieID_list = []
    RatingScore_list = []
    for row in results:
        UserID_list.append(row[4])
        MovieID_list.append(row[3])
        RatingScore_list.append(row[1])
    ratings_df = pd.DataFrame({"userId":UserID_list,"movieId":MovieID_list,"rating":RatingScore_list})
    # convert the User-Movie matrix
    print("to convert the User-Movie matrix...")
    ratings_matrix = ratings_df.pivot_table(index=["userId"], columns=["movieId"], values="rating")
    # print(ratings_matrix)
    # compute User-User similary matrix
    print("compute User-User similary matrix...")
    user_similar = ratings_matrix.T.corr()
    # print(user_similar)

    # compute Movie-Movie similary matrix
    print("compute Movie-Movie similary matrix...")
    movie_similar = ratings_matrix.corr()
    # print(movie_similar)

    cursor = connection.cursor()
    try:
        movies = cursor.execute('SELECT * FROM library_movies')
        results = cursor.fetchall()
    finally:
        cursor.close()
    MovieID_list = []
    MovieTitle_list = []
    MovieGenres_list = []
    for row in results:
        MovieID_list.append(row[0])
        MovieTitle_list.append(row[1])
        MovieGenres_list.append(row[2])
    movies_df = pd.DataFrame({"movieId": MovieID_list, "title": MovieTitle_list, "genres": MovieGenres_list})

    # function: convert movieName to movieID
    def movieToID(movies_df, name):
        id = list(movies_df.loc[movies_df["title"] == name]["movieId"].values)[0]
        return id

    ids_list = []
    for movieName in in_movieName_list:
        id = movieToID(movies_df, movieName.strip())
        print(id)
        ids_list.append(id)
    print(ids_list)
    # assume let userID=1 to watch movie list as movieID=[5, 22, 15, 79, 55]
    test_userID = in_userID
    test_movieID_list = ids_list
    print("test user and pre to watch movie list has been set...")

    # get movie similar list base on test movie has been given.
    final_result = []
    for movie in test_movieID_list:
        print("current preccess movieID is %d" % movie)
        similar_movie = movie_similar[movie].drop([movie]).dropna()
        similar_movie = similar_movie.where(similar_movie > 0).dropna()
        print(similar_movie)
        if similar_movie.empty is True:
            raise Exception("no similar movie base on <%d>" % movie)

        # match the test userID' info
        print("match the test userID' info...")
        ids = set(ratings_matrix.loc[int(test_userID)].dropna().index) & set(similar_movie.index)
        similar_movie = similar_movie.loc[list(ids)]

        print("Sort by similarity...")
        similar_values = []
        for i in similar_movie.index:
            similar_values.append(similar_movie.loc[i])

        similar_movie_data = {"movieID": similar_movie.index, "similar": similar_values}
        similar_movie_df = pd.DataFrame(similar_movie_data).sort_values(by="similar", ascending=False)
        print(similar_movie_df.head())

        # Collect statistics on the top 10 movies with the highest similarity to obtain the average score.
        def getMeanRating(movie_id):
            rating = list(ratings_df.loc[ratings_df["movieId"] == movie_id]["rating"].values)
            rating_ave = np.mean(rating)
            return rating_ave

        def getTopKMovie(similar_movie_df):
            return similar_movie_df[:20]

        similar_movie_df = getTopKMovie(similar_movie_df)

        print("Collect statistics on the top 10 movies with the highest similarity to obtain the average score...")
        top_similar_movie_av_list = []
        for id in list(similar_movie_df["movieID"]):
            top_similar_movie_av_list.append(getMeanRating(id))

        top_similar_movie_avg = np.mean(top_similar_movie_av_list)
        final_result.append(top_similar_movie_avg)
    print("predict ratings on new movie is : %d" % np.mean(final_result))

    context = {
        'in_userID' : in_userID,
        'in_movieID': in_movieID,
        'predict_ratings': round(np.mean(final_result),2),
    }
    return render(request, 'library/predicting_ratings.html', context=context)

def predicting_personality_traits(request):
    print(type(request))
    in_userID = request.POST["userID"]
    cursor = connection.cursor()
    try:
        ratings = cursor.execute('SELECT * FROM library_ratings')
        results = cursor.fetchall()
    finally:
        cursor.close()
    UserID_list = []
    MovieID_list = []
    RatingScore_list = []
    for row in results:
        UserID_list.append(row[4])
        MovieID_list.append(row[3])
        RatingScore_list.append(row[1])
    ratings_df = pd.DataFrame({"userId": UserID_list, "movieId": MovieID_list, "rating": RatingScore_list})
    cursor = connection.cursor()
    try:
        ratings = cursor.execute('SELECT * FROM library_tags')
        results = cursor.fetchall()
    finally:
        cursor.close()
    UserID_list = []
    MovieID_list = []
    TagContent_list = []
    for row in results:
        UserID_list.append(row[4])
        MovieID_list.append(row[3])
        TagContent_list.append(row[1])
    tags_df = pd.DataFrame({"userId": UserID_list, "movieId": MovieID_list, "tag": TagContent_list})
    print(tags_df.head())
    tags_list = recommend_service.predicting_personality_traits(in_userID, ratings_df, tags_df)

    context = {
        'in_userID': in_userID,
        'tags_list': tags_list
    }
    return render(request, 'library/predicting_presonality_traits.html', context=context)