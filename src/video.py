import os
from googleapiclient.discovery import build


class Video:
    API_KEY: str = os.getenv('API_KEY')

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.API_KEY)

    def __init__(self, video_id: str):
        self.__video_id = video_id

        self.response = (self.get_service().videos().list(id=self.__video_id, part='snippet,statistics').execute())
        self.video_title: str = self.response['items'][0]['snippet']['title']
        self.url: str = f"https://youtube/{self.__video_id}"
        self.view_count: int = self.response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id