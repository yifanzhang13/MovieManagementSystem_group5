from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.MoviesView, name='movies'),
    path('sorted/', views.AlphabetSortedMoviesView, name='sorted-movies'),
    path('reverse-sorted/', views.ReverseAlphabetSortedMoviesView, name='reverse-sorted-movies'),
    path('popular-movies/', views.PopularMoviesView, name='popular-movies'),
    path('polarising-movies/', views.PolarisingMoviesView, name='polarising-movies'),
    path('movies/<int:pk>', views.MovieDetail, name='movie-detail'),
    path('search/', views.search, name='search'),
    path('handle/', views.handle, name='handle'),
    path('audience-classification/', views.audience_classification, name='audience-classification'),
    path('predicting-ratings/', views.predicting_ratings, name='predicting-ratings'),
    path('to-predicting-ratings/', views.to_predicting_ratings, name='to-predicting-ratings'),
    path('predicting-personality-traits/', views.predicting_personality_traits, name='predicting-personality-traits'),
    path('to-predicting-personality-traits/', views.to_predicting_personality_traits, name='to-predicting-personality-traits'),
    # path('movies/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail')
]
