from django.urls import path
from . import views
app_name='library'
urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.MoviesView, name='movies'),
    path('movies/<int:pk>', views.MovieDetail, name='movie-detail'),
    path('search/', views.search, name='search'),
    path('handle/', views.handle, name='handle'),
    # path('movies/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail')
]
