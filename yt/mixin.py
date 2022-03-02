from googleapiclient.discovery import build
import re
from datetime import timedelta
from django.conf import settings
from youtubesearchpython import VideosSearch,ChannelsSearch

def title_formatting(title):

	if len(title) >= 30:
		return f'{title[0:20]}...'
	else:
		return title

class Youtube:

    def __init__(self,*args,**kwargs):
            
            self.api_service_name =settings.API_SERVICE_NAME
            self.api_version =settings.API_VERSION
            self.developer_key = settings.GOOGLE_API_KEY
            self.youtube=build(self.api_service_name,self.api_version,developerKey=self.developer_key)


    def stats(self,channel_id):
        channel_stats=self.youtube.channels().list(part='statistics',id=channel_id)
        channel_details=channel_stats.execute()
        return channel_details['items'][0]['statistics']



    def get_channel_stats(self,channel_id):
        all_data = []
        request = self.youtube.channels().list(
                    part='snippet,contentDetails,statistics',
                    id=channel_id)
        response = request.execute() 
        
        for i in range(len(response['items'])):
            data = dict(Channel_name = title_formatting(response['items'][i]['snippet']['title']),
                        Subscribers = response['items'][i]['statistics']['subscriberCount'],
                        Views = response['items'][i]['statistics']['viewCount'],
                        Total_videos = response['items'][i]['statistics']['videoCount'],
                        playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
            all_data.append(data)
        
        return all_data

        
    def get_video_ids(self, playlist_id):
        request = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId = playlist_id,
                    maxResults = 50)
        response = request.execute()
        
        video_ids = []
        
        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
        next_page_token = response.get('nextPageToken')
        more_pages = True
        
        while more_pages:
            if next_page_token is None:
                more_pages = False
            else:
                request = self.youtube.playlistItems().list(
                            part='contentDetails',
                            playlistId = playlist_id,
                            maxResults = 50,
                            pageToken = next_page_token)
                response = request.execute()
        
                for i in range(len(response['items'])):
                    video_ids.append(response['items'][i]['contentDetails']['videoId'])
                
                next_page_token = response.get('nextPageToken')
            
        return video_ids
    
    def get_video_details(self,video_ids):
        hour_pattern=re.compile(r'(\d+)H')
        minutes_pattern=re.compile(r'(\d+)M')
        seconds_pattern=re.compile(r'(\d+)S')   
        all_video_stats = []
        total_seconds=0
        tot_vid_seconds=0
        
        
        for i in range(0,len(video_ids), 50):
            request = self.youtube.videos().list(
                        part='snippet,statistics ,contentDetails',
                        id=','.join(video_ids[i:i+50]))
            response = request.execute()
            #print(response)
            
            for video in response['items']:
                duration=video['contentDetails']['duration']

                hours=hour_pattern.search(duration)
                minutes=minutes_pattern.search(duration)
                seconds=seconds_pattern.search(duration)
            

                hours=int(hours.group(1)) if hours else 0
                minutes=int(minutes.group(1)) if minutes else 0
                seconds=int(seconds.group(1)) if seconds else 0

                vid_seconds=timedelta(
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds

                ).total_seconds()
                
                total_vid_seconds=timedelta(
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds

                ).total_seconds()

            
                

                tot_vid_seconds+=total_vid_seconds
                
                total_seconds+=vid_seconds
                total_seconds=int(total_seconds)
                minutes,seconds=divmod(total_seconds,60)
                hours,minutes=divmod(minutes,60)
                
                try :
                    video_stats = dict(link=video['id'],
                                            Title = title_formatting(video['snippet']['title']),
                                            Duration=f'{hours}:{minutes}:{seconds}',
                                        Published_date = video['snippet']['publishedAt'],
                                        Views =int( video['statistics']['viewCount']),
                                        Likes =int( video['statistics']['likeCount']),
                                        Comments = int(video['statistics']['commentCount']),
                                        )
                except:
                    pass
                
                all_video_stats.append(video_stats)
                total_seconds=0
        tot_vid_seconds=int(tot_vid_seconds)
        minutes,seconds=divmod(tot_vid_seconds,60)
        hours,minutes=divmod(minutes,60)
        tot_time=f'{hours}:{minutes}:{seconds}'
        return all_video_stats, tot_time

    def get_playlists(self, channel_id):
            nextPageToken=None
            playlist_details = []
            
            
            request = self.youtube.playlists().list(
                    part="snippet",
                    channelId=channel_id,maxResults=50,
                    pageToken=nextPageToken)
            response = request.execute()
                
            for i in range(len(response['items'])):
                video_details=dict(playlist_id=response['items'][i]['id'], 
                                description=response['items'][i]['snippet']['title'])
                playlist_details.append(video_details)
                
            
            next_page_token = response.get('nextPageToken')
            more_pages = True

            while more_pages:
                if next_page_token is None:
                    more_pages = False
                else:
                    request = self.youtube.playlists().list( part="snippet",
                    channelId=channel_id,maxResults=50,
                    pageToken=nextPageToken)
                response = request.execute()
                video_details=dict(playlist_id=response['items'][i]['id'], 
                                description=response['items'][i]['snippet']['title'])
                playlist_details.append(video_details)
            
                next_page_token = response.get('nextPageToken')

            return  playlist_details

    def search(self, keyword):
        channelsSearch = ChannelsSearch(keyword)
        return channelsSearch.result()
        


     

