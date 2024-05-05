from googleapiclient.discovery import build
from datetime import datetime
import os

# Set up YouTube Data API credentials
api_key = os.environ.get("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)
# In views.py
from django.shortcuts import render
from django.http import JsonResponse
from model import Video
from . import get_videos_by_category, get_transcript



def fetch_and_store_videos(request):
    categories = ['Top stories', 'Sports', 'Entertainment', 'Science', 'Health', 'Business', 'Technology', 'National', 'World']
    response_data = []  # List to store video data
    for category in categories:
        videos = get_videos_by_category(category)
        for video in videos:
            video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
            transcript = get_transcript(video['id']['videoId'])
            channel = video['snippet']['channelTitle']
            publication_date = video['snippet']['publishedAt']
            category = category
            # Check if the video already exists in the database
            if not Video.objects.filter(video_url=video_url).exists():
                Video.objects.create(
                    video_url=video_url,
                    transcript=transcript,
                    channel=channel,
                    publication_date=publication_date,
                    category=category
                )
                send_video = {
                    'video_url':video_url,
                    'transcript':transcript,
                    'channel': channel,
                    'publication_date':publication_date,
                    'category' : category
                }
                response_data.append(send_video)  # Add video data to the response list
    
    return JsonResponse(response_data, safe=False)  # Return the entire list as JSON


# Define function to retrieve videos by category
def get_videos_by_category(category, max_results=10):
    request = youtube.search().list(
        part='snippet',
        q='',
        type='video',
        videoCategoryId=category,
        maxResults=max_results
    )
    response = request.execute()
    return response['items']

# Define function to get transcript of a video
def get_transcript(video_id):
    request = youtube.captions().list(
        part='snippet',
        videoId=video_id
    )
    response = request.execute()
    if 'items' in response:
        caption_id = response['items'][0]['id']
        caption_request = youtube.captions().download(
            id=caption_id,
            tfmt='ttml'
        )
        caption_response = caption_request.execute()
        return caption_response.decode('utf-8')
    else:
        return None



# Define Django models
from django.db import models
from celery import shared_task
import openai

class Video(models.Model):
    video_url = models.URLField()
    transcript = models.TextField(null=True)
    channel = models.CharField(max_length=100)
    publication_date = models.DateTimeField()
    category = models.CharField(max_length=100)

    class Meta:
        unique_together = ('video_url', 'publication_date',)


@shared_task
def summarize_transcripts():
    videos = Video.objects.all()
    for video in videos:
        if not video.summary:  # Check if summary already exists
            # Call OpenAI API to summarize the transcript
            summary = openai.Completion.create(
                engine="text-davinci-002",
                prompt=video.transcript,
                max_tokens=100
            ).choices[0].text.strip()
            video.summary = summary
            video.save()


from django.http import JsonResponse

def summarize(request):
    video_id = request.GET.get('video_id')
    video = Video.objects.get(id=video_id)
    if not video.summary:
        # Trigger Celery task to summarize transcript
        summarize_transcripts.delay()
    return JsonResponse({'transcript': video.transcript, 'summary': video.summary})




def chat(request):
    query = request.GET.get('query')
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=query,
        max_tokens=50
    ).choices[0].text.strip()
    return JsonResponse({'response': response})


