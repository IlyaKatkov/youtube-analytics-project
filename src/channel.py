from googleapiclient.discovery import build
import os
import json




class Channel:
    """Класс для ютуб-канала"""

    API_KEY = os.getenv('API_KEY')
    service = build('youtube', 'v3', developerKey=API_KEY)
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id



    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        r = self.service.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(r, indent=2, ensure_ascii=False))