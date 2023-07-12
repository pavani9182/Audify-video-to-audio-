from django import forms
from django.db import models
from .models import *
from pytz import timezone
from datetime import datetime
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import os

from urllib.parse import urlparse
import uuid

class VideoUploadForm(forms.ModelForm):
    video_file = forms.FileField(required=False)
    video_link = forms.URLField(required=False)
    
    class Meta:
        model = Video
        fields = ('title', 'video_file','video_link')

class CommentUploadForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comments','timestamps')

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class VideoLinkUploadForm(forms.ModelForm):
    class Meta:
        model = VideoLinks
        fields = ('video_link', 'title')
class CommentLinkForm(forms.ModelForm):
    class Meta:
        model = CommentLinks
        fields = ('comments','timestamps')