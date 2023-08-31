from googleapiclient.discovery import build
import os
import json




class Channel:

    API_KEY: str = os.getenv('API_KEY')


    @classmethod
    def get_service(cls):
        """Dозвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=cls.API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        self.response = (self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute())

        self.title: str = self.response['items'][0]['snippet']['title']
        self.channel_description: str = self.response['items'][0]['snippet']['description']
        self.url: str = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count: int = int(self.response['items'][0]['statistics']['subscriberCount'])
        self.video_count: int = int(self.response['items'][0]['statistics']['videoCount'])
        self.view_count: int = int(self.response['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def print_info(self) -> None:
        """Выводит информацию о канале"""
        print(json.dumps(self.response, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        self.__channel_id = channel_id
    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.response, f, ensure_ascii=False)