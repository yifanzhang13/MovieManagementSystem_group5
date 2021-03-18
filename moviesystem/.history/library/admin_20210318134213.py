from django.contrib import admin

# Register your models here.

from .models import Movies, Users, Ratings, Links, Tags

# register models
# admin.site.register(Movies)
admin.site.register(Users)
admin.site.register(Ratings)
admin.site.register(Links)
admin.site.register(Tags)

@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('MovieGenres')