from django.db import models

# Create your models here.
class movies(models.Model):
    # Fields
    MovieID = models.IntegerField(primary_key = True)
    MovieTitle = models.CharField(max_length=255)
    MovieGenres = models.CharField(max_length=255)