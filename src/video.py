import json
import os

from googleapiclient.discovery import build
from dotenv import load_dotenv

import isodate

load_dotenv()


class Video:
    KEY = os.getenv('YOUTUBE_KEY')
    youtube = build('youtube', 'v3', developerKey=KEY)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id

        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.video_id
                                                         ).execute()

        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.video_url: str = 'https://youtu.be/gaoc9MPZ4bw'
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.video_response, indent=2, ensure_ascii=False))

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
