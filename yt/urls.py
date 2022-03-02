from django.urls import path

from .views import ( 
                     ytview,result,playlist,playlist_details,
                     result_comments,result_likes,searchresults,
                     result_dates
                     )       

app_name='yt'

urlpatterns = [
    path('',ytview,name='yt'),
    path('yt/results_views',result,name='result-views'),
    path('yt/results_comments',result_comments,name='result-comments'),
    path('yt/results_likes',result_likes,name='result-likes'),
    path('yt/results_dates',result_dates,name='result-dates'),
    path('yt/playlist',playlist,name='playlist'),
    path('yt/playlistdetail',playlist_details,name='playlistdetail'),
    path('yt/serchresults',searchresults,name='searchresults'),
]
    
