from django import forms

class SearchMovieForm(forms.Form):
    movie_to_be_searched = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")