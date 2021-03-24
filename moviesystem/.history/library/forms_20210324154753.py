from django import forms

class SearchMovieForm(forms.Form):
    searched_movie = forms.CharField(max_length=225, required=False)

    def clean_search_movie(self):
        data = self.cleaned_data['searched_movie']
        if len(data)>225 or len(data)<=0:
            raise ValidationError(('Invalid length of input movie name'))

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data