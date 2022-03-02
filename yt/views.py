from django.http import HttpResponse
from django.shortcuts import render
import os
from googleapiclient.discovery import build
from .forms import Fooform
#from .helper import youtube_api,youtube,get_channel_stats,get_video_ids,get_video_details
from .mixin import Youtube
from datetime import datetime


# Create your views here.
details=Youtube()

def ytview(request):

    form = Fooform(request.POST,None)
    
    
    context={"form":form}

    return render(request, "yt/index.html",context)

def result(request):
    form = Fooform(request.POST,None)
     
    channelname=request.POST.get("channelname")
      
    channel_stats=details.get_channel_stats(channelname)
    channel_id=channel_stats[0]['playlist_id']
    video_ids=details.get_video_ids(channel_id)
    video_details=details.get_video_details(video_ids)
    videos=video_details[0]
    total_time=video_details[1]
    print(total_time)
    videos.sort(key=lambda vid:vid['Views'],reverse=True)
    toptenvideo=[]
    for video in videos[:40]:
        video['Published_date']=video['Published_date'].split('T')[0]
        toptenvideo.append(video)
    context={'videos':video_details,"videos":videos,"video_ids":video_ids,"toptenvideo":toptenvideo,"channel_stats":channel_stats,"channelname":channelname,"total_time": total_time}
    return render(request, "yt/result_views.html",context)

def result_comments(request):
    form = Fooform(request.POST,None)
    channelname=request.POST.get("channelname")

    channel_stats=details.get_channel_stats(channelname)
    channel_id=channel_stats[0]['playlist_id']
    video_ids=details.get_video_ids(channel_id)
    video_details=details.get_video_details(video_ids)
    videos=video_details[0]
    total_time=video_details[1]
    print(total_time)
    videos.sort(key=lambda vid:vid['Comments'],reverse=True)
    toptenvideo=[]
    for video in videos[:40]:
        video['Published_date']=video['Published_date'].split('T')[0]
        toptenvideo.append(video)
    context={'videos':video_details,"videos":videos,"video_ids":video_ids,"toptenvideo":toptenvideo,"channel_stats":channel_stats,"channelname":channelname,"total_time": total_time}
    return render(request, "yt/result_comments.html",context)

def result_likes(request):
    form = Fooform(request.POST,None)
    
    channelname=request.POST.get("channelname")
       
    channel_stats=details.get_channel_stats(channelname)
    channel_id=channel_stats[0]['playlist_id']
    video_ids=details.get_video_ids(channel_id)
    video_details=details.get_video_details(video_ids)
    videos=video_details[0]
    total_time=video_details[1]
    print(total_time)
    videos.sort(key=lambda vid:vid['Likes'],reverse=True)
    toptenvideo=[]
    for video in videos[:40]:
        video['Published_date']=video['Published_date'].split('T')[0]
        toptenvideo.append(video)
    context={'videos':video_details,"videos":videos,"video_ids":video_ids,"toptenvideo":toptenvideo,"channel_stats":channel_stats,"channelname":channelname,"total_time": total_time}
    return render(request, "yt/result_likes.html",context)

def result_dates(request):
    form = Fooform(request.POST,None)
     
    channelname=request.POST.get("channelname")
       
    channel_stats=details.get_channel_stats(channelname)
    channel_id=channel_stats[0]['playlist_id']
    video_ids=details.get_video_ids(channel_id)
    video_details=details.get_video_details(video_ids)
    videos=video_details[0]
    total_time=video_details[1]
    print(total_time)
    videos.sort(key=lambda vid:vid['Published_date'],reverse=True)
    toptenvideo=[]
    for video in videos[:12]:  
        video['Published_date']=video['Published_date'].split('T')[0]      
        toptenvideo.append(video)
    context={'videos':video_details,"videos":videos,"video_ids":video_ids,"toptenvideo":toptenvideo,"channel_stats":channel_stats,"channelname":channelname,"total_time": total_time}
    return render(request, "yt/result_dates.html",context)

def playlist(request):
    
    
    # username = request.POST.get("username")
    channelname=request.POST.get("channelname")
    
    playlist=details.get_playlists(channelname)
    
    context={'channelname':channelname,"playlist":playlist}
    return render(request, "yt/playlist.html",context)
    

def playlist_details (request):
        
          
        playlist_id=request.GET.get('playlist_id')
        print(playlist_id)
        vid_details=details.get_video_ids(playlist_id)
        get_vid_details=details.get_video_details(vid_details)
        videos=get_vid_details[0]
        total_time=get_vid_details[1]
        videos.sort(key=lambda vid:vid['Views'],reverse=True)
        for video in videos:  
            video['Published_date']=video['Published_date'].split('T')[0]

        context={"hello":"hello","videos":videos,"total_time":total_time}
        return render(request, "yt/playlistdetail.html",context)

def searchresults(request):
    
    keyword= request.GET.get("keyword")
    results=details.search(keyword)
    
    context={"results":results}
    print(keyword)
    return render(request, "yt/serchresults.html",context)




