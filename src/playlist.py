import datetime
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

        self.playlist_id = playlist_id
        self.title = self.get_title()

        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def get_title(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='snippet',
                                                            maxResults=50,
                                                            ).execute()
        title = playlist_videos['items'][0]['snippet']['title'].split('.')[0]
        return title

    def get_playlist(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        return video_ids

    @property
    def total_duration(self):
        duration_list = []
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.get_playlist())
                                                    ).execute()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_list.append(duration)

        result = sum(duration_list, datetime.timedelta())
        return result

    def show_best_video(self):
        like_list = []
        for video in self.get_playlist():
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video
                                                        ).execute()

            like_count: int = video_response['items'][0]['statistics']['likeCount']
            like_list.append(like_count)
        like = max(like_list)
        index_like = like_list.index(like)
        return f"https://youtu.be/{self.get_playlist()[index_like]}"
