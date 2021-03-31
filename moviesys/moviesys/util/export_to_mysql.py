# -*- coding:utf-8 -*-
__version__ = '1.0.0.0'

import django
import os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moviesystem.settings")
django.setup()


from library.models import *

def export_to_user_data():
    user_df = pd.read_csv(r'users.csv', engine='python')
    user_df.columns = ['UserID']
    for index, row in user_df.iterrows():
        obj = Users.objects.create(UserID=row['UserID'])
        obj.save()


def export_movie_data():

    Movies.objects.all().delete()
    movies = pd.read_csv(r'movies.csv', sep=",", engine='python')
    movies.columns = ['movieId', 'title', 'genres']
    for index, row in movies.iterrows():
        Movies.objects.create(MovieID=row['movieId'],MovieTitle=row['title'], MovieGenres=row['genres'])


def export_ratings_data():
    Ratings.objects.all().delete()
    ratings = pd.read_csv(r'ratings.csv', sep=",", engine='python')
    ratings.columns = ['userId','movieId','rating','timestamp']
    for index, row in ratings.iterrows():
        try:
            user = Users.objects.get(UserID=row['userId'])
            movie = Movies.objects.get(MovieID=row['movieId'])
            Ratings.objects.create(UserID=user, MovieID=movie, RatingScore=int(row['rating']), Timestamp=row['timestamp'])
        except Exception as e:
            print(e)


def export_tags_data():
    Tags.objects.all().delete()
    ratings = pd.read_csv(r'tags.csv', sep=",", engine='python')
    ratings.columns = ['userId','movieId','tag','timestamp']
    for index, row in ratings.iterrows():
        try:
            user = Users.objects.get(UserID=row['userId'])
            movie = Movies.objects.get(MovieID=row['movieId'])
            Tags.objects.create(UserID=user, MovieID=movie, TagContent=row['tag'], Timestamp=row['timestamp'])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # export_to_user_data()
    export_movie_data()
    export_ratings_data()
    export_tags_data()
