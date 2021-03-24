from django import forms

class SearchMovieForm(forms.Form):
    searched_movie = forms.CharField(max_length=225, required=False)

    def clean_search_movie(self):
        data = self.cleaned_data['searched_movie']
        if len(data)>225 or len(data)<=0:
            raise ValidationError(('Invalid length of input movie name'))
        return data