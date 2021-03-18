from django.db import models

# Create your models here.
class movies(models.Model):
    # Fields
    MovieID = models.IntegerField(primary_key = True)
    MovieTitle = models.CharField(max_length=255)
    MovieGenres = models.CharField(max_length=255)

class users(models.Model):
    # Fields
    UserID = models.IntegerField(primary_key = True)

class tags(models.Model):
    # Fields
    UserID = models.ForeignKey('users', to_field=users.UserID, on_delete=models.PROTECT)
    MovieID = models.ForeignKey('movies', to_field=movies.MovieID, on_delete=models.PROTECT)
    TagContent = models.CharField(max_length=255)
    Timestamp = models.IntegerField()

class links(models.Model):
    # Fields
    MovieID = models.ForeignKey('movies', to_field=movies.MovieID, on_delete=models.PROTECT)
    