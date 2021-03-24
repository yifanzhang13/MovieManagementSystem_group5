from django import forms

class SearchMovieForm(forms.Form):
    movie_to_be_searched = forms.CharField(max_length=225, required=False)