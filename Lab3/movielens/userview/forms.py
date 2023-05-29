from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
class Meta:
    model = User
    fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class RatingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Rating
        fields = ['movie', 'value']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your comment here', 'rows': 4}),
        label=''
    )
    class Meta:
        model = Comment
        fields = ('content',)

class SearchForm(forms.Form):
    genres = forms.CharField(required=False)
    title = forms.CharField(required=False)
    min_rating = forms.IntegerField(required=False)
    
class MovieForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Movie
        fields = ['title', 'genres' ,'imdblink']

# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['title', 'img', 'front_image', 'movie']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'img', 'front_image']

    # def __init__(self, movie, *args, **kwargs):
    #     super(ImageForm, self).__init__(*args, **kwargs)
    #     self.movie = movie

    # def save(self, commit=True):
    #     image = super(ImageForm, self).save(commit=False)
    #     image.movie = self.movie
    #     if commit:
    #         image.save()
    #     return image