import os
import uuid
from pytube import YouTube
import os
import uuid
import datetime
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.files import File
from .forms import *
from moviepy.editor import VideoFileClip
from datetime import timedelta
from django.core.files.temp import NamedTemporaryFile
from .models import *
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# import youtube_dl
from pytube import YouTube
@login_required(login_url='login')
def delete_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video.delete()
    return redirect('video_list')
def delete_link(request, link_id):
    link = get_object_or_404(VideoLinks, pk=link_id)
    link.delete()
    return redirect('video_list')
def save_comments(request):
    if request.method == 'POST':
        video_id = request.POST.get('video_id')  # Assuming you have a unique identifier for the video
        comments = request.POST.get('comments')
        timestamp = request.POST.get('timestamp')

        # Retrieve the video object based on the video_id
        video = Video.objects.get(id=video_id)

        # Append the new comments and timestamp to the existing ones
        video.comments += '\n' + comments
        video.timestamps += '\n' + timestamp

        # Save the updated video object
        video.save()

        return JsonResponse({'message': 'Comments saved successfully.'})

    return JsonResponse({'error': 'Invalid request method.'})
def convert_to_audio(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path, codec='pcm_s16le')
    video_clip.close()
    audio_clip.close()

@login_required(login_url='login')

def dashboard(request):
    customer = request.user.customer  # Retrieve the customer model of the current user
    videos = Video.objects.filter(customer=customer)  # Filter videos based on the customer
    links = VideoLinks.objects.filter(customer=customer)
    no_of_videos=videos.count()
    context = {'videos':videos,'no':no_of_videos,'links':links}
    return render(request, 'accounts/dashboard.html',context)

def format_duration(duration_seconds):
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = duration_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.customer = request.user.customer  # Assign the current user's customer model
            video.save()
            

            video_path = video.video_file.path
            
            

            # Get the duration of the video
            clip = VideoFileClip(video_path)
            duration_seconds = int(clip.duration)
            clip.close()

            # Convert duration to hh:mm:ss format
            duration_formatted = format_duration(duration_seconds)

            # Save the duration in the model
            video.duration = duration_formatted
            video.save()

            # Generate unique name for audio file
            audio_filename = f"{uuid.uuid4()}.wav"

            # Specify the output directory for audio files
            audio_output_dir = os.path.join(settings.MEDIA_ROOT, 'audios/')

            # Create the output directory if it doesn't exist
            os.makedirs(audio_output_dir, exist_ok=True)

            # Specify the output path for the audio file
            audio_output_path = os.path.join(audio_output_dir, audio_filename)
            print(audio_output_path)
            # Convert video to audio
            convert_to_audio(video_path, audio_output_path)

            # Save the audio file path in the model
            video.audio_file.name = os.path.join('audios', audio_filename)
            video.audio_fileName = audio_filename
            video.save()

            return redirect('video_list')

    else:
        form = VideoUploadForm()
        return render(request, 'accounts/home.html', {'form': form})


@login_required(login_url='login')
def audio_page(request, audio_fileName):
    video = get_object_or_404(Video, audio_fileName=audio_fileName)

    if request.method == "POST":
        form = CommentUploadForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.customer = request.user.customer  # Assign the current user's customer model  
            comment.video = video  # Associate the comment with the video
            comment.save()
            return redirect(request.path)
    else:
        form = CommentUploadForm()

    comments = Comments.objects.filter(video=video)  # Retrieve comments for the video
    context = {'video': video, 'form': form, 'comments': comments}
    return render(request, 'accounts/audio_page.html', context)

@login_required(login_url='login')
def audio_page_links(request , audio_fileName):
    links = get_object_or_404(VideoLinks, audio_fileName=audio_fileName)
    if request.method == "POST":
        form = CommentLinkForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.customer = request.user.customer
            comment.video_link = links 
            comment.save()
            return redirect(request.path)
    else:
        form = CommentLinkForm()
    comments = CommentLinks.objects.filter(video_link=links)
    context = {'links':links,'comments':comments,'form':form}
    return render(request, 'accounts/audio_page_links.html',context)
    

@unauthenticated_user
def register_page(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            Customer.objects.create(user=user,name=user.username)
            
            messages.success(request, 'Account was created for ' +username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html',context)

@unauthenticated_user
def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
            return render(request, 'accounts/login.html')
    
    return render(request, 'accounts/login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def upload_youtube_video(request):
    if request.method == 'POST':
        form = VideoLinkUploadForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            video_link = form.cleaned_data['video_link']
            title = form.cleaned_data['title']
            customer = request.user.customer  # Retrieve the customer model of the current user

            # URL input from the user
            yt = YouTube(video_link)
            video_path = yt.streams.first().download()
            clip = VideoFileClip(video_path)
            duration_seconds = int(clip.duration)
            clip.close()
            duration_formatted = format_duration(duration_seconds)
            link.duration = duration_formatted

            
            # Extract audio only
            video = yt.streams.filter(only_audio=True).first()

            # Replace 'destination' with the path where you want to save the download file
            destination = "/Desktop/Manideep/Projects/videotoaudio/audios"

            # Generate a UUID-based filename
            audio_filename = str(uuid.uuid4()) + '.mp3'

            # Download the file
            out_file = video.download(output_path=destination)

            # Save the file with the generated filename
            new_file = os.path.join(destination, audio_filename)
            os.rename(out_file, new_file)

            # Calculate the duration of the video
            

            # Save the video link and other details in the VideoLinks model
            link.audio_file.save(audio_filename, open(new_file, 'rb'))
            link.audio_fileName = audio_filename
            link.title = title
            link.customer = customer
            # Set the video_file field with the downloaded video file
            link.video_file = os.path.join('videos', os.path.basename(video_path))
            link.save()
            # Result of success

            return redirect('video_list')
    else:
        form = VideoLinkUploadForm()

    context = {'form': form}
    return render(request, 'accounts/upload_youtube_video.html', context)
