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

        self.title = self.get_info_video()[0]
        self.videview_count = self.get_info_video()[1]
        self.like_count = self.get_info_video()[2]

        self.video_url: str = 'https://youtu.be/gaoc9MPZ4bw'

    def get_info_video(self):
        list_info = []
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=self.video_id
                                                        ).execute()

            video_title: str = video_response['items'][0]['snippet']['title']
            view_count: int = video_response['items'][0]['statistics']['viewCount']
            like_count: int = video_response['items'][0]['statistics']['likeCount']
            list_info.append(video_title)
            list_info.append(view_count)
            list_info.append(like_count)
        except IndexError:
            list_info.append(None)
            list_info.append(None)
            list_info.append(None)
        return list_info

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
