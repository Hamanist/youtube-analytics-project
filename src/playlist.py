import os
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv

import isodate

load_dotenv()


class PlayList:
    KEY = os.getenv('YOUTUBE_KEY')
    youtube = build('youtube', 'v3', developerKey=KEY)

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                                 part='snippet',
                                                                 maxResults=50,
                                                                 ).execute()
        self.title = self.playlist_videos['items'][0]['snippet']['title'].split('.')[0]
        self.url = 'https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw'

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.playlist_videos, indent=2, ensure_ascii=False))

    def __str__(self):
        return self.playlist_videos

    def total_duration(self): ...
