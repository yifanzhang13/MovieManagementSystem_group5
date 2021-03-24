from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.MoviesView, name='movies')
    path('movies/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail')
]
