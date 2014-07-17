from django import forms

class poster(forms.Form):
    poster_name = forms.CharField(label="Poster Name:")
    path_of_poster = forms.ImageField()

class information(forms.Form):
    message = forms.CharField(label='Message:')
    thumb = forms.ImageField()


