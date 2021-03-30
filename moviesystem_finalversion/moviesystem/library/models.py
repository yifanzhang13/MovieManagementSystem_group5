from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances

# Create your models here.

class Movies(models.Model):
    # Fields
    MovieID = models.IntegerField(primary_key = True)
    MovieTitle = models.CharField(max_length=255)
    MovieGenres = models.CharField(max_length=255)

    class Meta:
        db_table="library_movies"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('movie-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.MovieTitle

class Users(models.Model):
    # Fields
    UserID = models.IntegerField(primary_key = True)

    class Meta:
        db_table="library_users"

    def __str__(self):
        """String for representing the Model object."""
        return str(self.UserID)

class Tags(models.Model):
    # Fields
    UserID = models.ForeignKey('Users', on_delete=models.PROTECT)
    MovieID = models.ForeignKey('Movies', on_delete=models.PROTECT)
    TagContent = models.CharField(max_length=255)
    Timestamp = models.IntegerField()

    class Meta:
        db_table="library_tags"

    def __str__(self):
        """String for representing the Model object."""
        return self.TagContent

class Links(models.Model):
    # Fields
    MovieID = models.ForeignKey('Movies', on_delete=models.PROTECT)
    imdbID = models.IntegerField()
    tmdbID = models.IntegerField()

    class Meta:
        db_table="library_links"

    def __str__(self):
        """String for representing the Model object."""
        return str(self.MovieID)

class Ratings(models.Model):
    # Fields
    UserID = models.ForeignKey('Users', on_delete=models.PROTECT)
    MovieID = models.ForeignKey('Movies', on_delete=models.PROTECT)
    RatingScore = models.IntegerField()
    Timestamp = models.IntegerField()

    class Meta:
        db_table="library_ratings"

    def __str__(self):
        """String for representing the Model object."""
        return str(self.MovieID)