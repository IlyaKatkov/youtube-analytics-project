from abc import ABC
import os
import datetime
import isodate
from googleapiclient.discovery import build



class Base_class(ABC):
    api_key: str = os.getenv('API_KEY')

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

class PlayList(Base_class):

    def __init__(self, playlist_id: str):
        self.__playlist_id = playlist_id
        self.playlist_json = (self.get_service().playlists().list(id=self.__playlist_id, part='snippet').execute())
        self.title = self.playlist_json['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails', maxResults=50,).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        max_likes = 0
        video_id = ''
        for video in self.video_response['items']:
            count_likes = int(video['statistics']['likeCount'])
            if max_likes < count_likes:
                max_likes = count_likes
                video_id = video['id']
        return f'https://youtu.be/{video_id}'