from django.contrib import admin

# Register your models here.

from .models import Movies, Users, Ratings, Links, Tags

# register models
# admin.site.register(Movies)
# admin.site.register(Users)
# admin.site.register(Ratings)
# admin.site.register(Links)
# admin.site.register(Tags)

@admin.register(Movies) # use the @register decorator to register the models
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('MovieID', 'MovieTitle', 'MovieGenres')

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('UserID')