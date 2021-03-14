from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# Register your models here.
admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    pass

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
