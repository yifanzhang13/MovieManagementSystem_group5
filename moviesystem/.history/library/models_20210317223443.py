from django.db import models

# Create your models here.
class Movies(models.Model):
    # Fields
    MovieID = models.IntegerField(primary_key = True)
    MovieTitle = models.CharField(max_length=255)
    MovieGenres = models.CharField(max_length=255)

class Users(models.Model):
    # Fields
    UserID = models.IntegerField(primary_key = True)

class Tags(models.Model):
    # Fields
    UserID = models.ForeignKey('users', to_field=users.UserID, on_delete=models.PROTECT)
    MovieID = models.ForeignKey('movies', to_field=movies.MovieID, on_delete=models.PROTECT)
    TagContent = models.CharField(max_length=255)
    Timestamp = models.IntegerField()

class Links(models.Model):
    # Fields
    MovieID = models.ForeignKey('movies', to_field=movies.MovieID, on_delete=models.PROTECT)
    imdbID = models.IntegerField()
    tmdbID = models.IntegerField()

class Ratings(models.Model)