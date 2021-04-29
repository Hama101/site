from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import *

class CreateUserForm(UserCreationForm):
    class Meta :
        model = User
        fields = [ "username" , "email" , "password1" , "password2" ]

class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user']


class UpdateToProForm(ModelForm):
    class Meta :
        model = Pro
        fields = '__all__'
        exclude = ['user']

class CommentForm(ModelForm):
    class Meta :
        model = Comment
        fields = ['body']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exlude = ['user']

