
from django.db import models
from pytz import timezone
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    profile_pic = models.ImageField(default='download.jpg',null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name or ''
    

class Video(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=8, blank=True, default='00:00:00')
    audio_file = models.FileField(upload_to='audios', null=True, blank=True)
    audio_fileName = models.CharField(max_length=200,blank=True)
    video_link = models.URLField()
    def uploaded_at_ist(self):
        utc_time = self.uploaded_at.replace(tzinfo=timezone('UTC'))
        ist_time = utc_time.astimezone(timezone('Asia/Kolkata'))
        return ist_time.strftime('%Y-%m-%d %H:%M:%S')
    def __str__(self):
        return self.title

class Comments(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comments = models.CharField(max_length=200)
    timestamps = models.CharField(max_length=200)
    def __str__(self):
        return self.comments
        # return self.video.title

class VideoLinks(models.Model):
    video_link = models.URLField(max_length=200)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=8, blank=True, default='00:00:00')
    audio_file = models.FileField(upload_to='audios', null=True, blank=True)
    audio_fileName = models.CharField(max_length=200,blank=True)
    def __str__(self):
        return self.title

class CommentLinks(models.Model):
    video_link = models.ForeignKey(VideoLinks, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    comments = models.CharField(max_length=200)
    timestamps = models.CharField(max_length=200)
    def __str__(self):
        return self.video_link.title