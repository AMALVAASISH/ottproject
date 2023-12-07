from django import forms
# importing from the django library the package forms
from django.contrib.auth.models import User

from .models import Post, Episode
 #creating a form class inheriting the class forms from package forms
class MyLoginForm(forms.Form):

    #Create two fields in the form for username and password
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    # profile_picture = forms.ImageField(label='Profile Picture', required=False)  # Add the ImageField

    class Meta:
        model = User
        fields = ('username','email','password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password doesnt match')

        return cd['password2']

class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','duration','description','Image','shortname','cast','movie_genre','movie_media_genre','video_url')


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','duration','description','Image','shortname','cast','movie_genre','movie_media_genre','video_url')

class EpisodeAddForm(forms.ModelForm):
    class Meta:
        model = Episode # the post model from models.py and its fields for user to input
        fields = ('title', 'description', 'video_url','duration','cast')

class EpisodeEditForm(forms.ModelForm):
    class Meta:
        model = Episode # the post model from models.py and its fields for user to input
        fields = ('title', 'description', 'video_url','duration','cast')