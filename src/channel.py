import os
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv

import isodate

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""
    KEY = os.getenv('YOUTUBE_KEY')
    youtube = build('youtube', 'v3', developerKey=KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]['snippet']['title']  # название канала
        self.description = self.channel["items"][0]['snippet']['description']  # описание канала
        self.url = f'https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A'  # URL
        self.subscribers = self.channel["items"][0]['statistics']['subscriberCount']  # подписчики
        self.video_count = self.channel["items"][0]['statistics']['videoCount']  # количество видео
        self.view_count = self.channel["items"][0]['statistics']['viewCount']  # просмотры

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, data_json):
        with open(data_json, 'w', encoding='utf8') as file:
            json.dump([
                {'title': self.title,
                 'description': self.description,
                 'url': self.url,
                 'subscribers': self.subscribers,
                 'video_count': self.video_count,
                 'view_count': self.view_count}
            ], file, indent=2, ensure_ascii=False)
