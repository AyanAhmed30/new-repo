from django import forms
from .gee import data_gee
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm



class dataset_geemap(forms.Form):
    data, f = data_gee()

    options = [(row['id'], row['title']) for index, row in data.iterrows()]
    option = forms.ChoiceField(choices=options)



class SignUpForm (UserCreationForm):
    class Meta:
        model=User
        fields = {'username','email', 'password1', 'password2'}