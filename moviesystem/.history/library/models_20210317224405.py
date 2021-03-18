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
    UserID = models.ForeignKey('Users', to_field=Users.UserID, on_delete=models.PROTECT)
    MovieID = models.ForeignKey('Movies', to_field=Movies.MovieID, on_delete=models.PROTECT)
    TagContent = models.CharField(max_length=255)
    Timestamp = models.IntegerField()

class Links(models.Model):
    # Fields
    MovieID = models.ForeignKey('Movies', on_delete=models.PROTECT)
    imdbID = models.IntegerField()
    tmdbID = models.IntegerField()

class Ratings(models.Model):
    # Fields
    UserID = models.ForeignKey('Users', to_field=Users.UserID, on_delete=models.PROTECT)
    MovieID = models.ForeignKey('Movies', to_field=Movies.MovieID, on_delete=models.PROTECT)
    RatingScore = models.IntegerField()
    Timestamp = models.IntegerField()