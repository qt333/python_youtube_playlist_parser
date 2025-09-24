import os
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import json
from datetime import datetime as dt
from os import getenv
import requests

from dotenv import load_dotenv

load_dotenv()

DEV_KEY = getenv('DEV_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')
PLAYLIST_NAME = os.getenv('PLAYLIST_NAME', '1')

date = dt.now().strftime("%d-%m-%Y")

# update the working directory
root_dir = os.getcwd() + os.sep

# url = input("Enter youtube playlist id : ")
# query = parse_qs(urlparse(url).query, keep_blank_values=True)
# print(query)
# playlist_id = query["list"][0]

print(f"get all playlist items links from {PLAYLIST_ID}")

# Update your Google API-KEY with the developerKey
youtube = googleapiclient.discovery.build(
    "youtube", "v3", developerKey=DEV_KEY
)

request = youtube.playlistItems().list(
    part="snippet", playlistId=PLAYLIST_ID, maxResults=50
)
response = request.execute()

playlist_items = []
while request is not None:
    response = request.execute()
    playlist_items += response["items"]
    request = youtube.playlistItems().list_next(request, response)

print("\n")
count = 1

youtube_playlist_titles = list()

for t in playlist_items:
    videoOwnerChannelTitle = t.get('snippet').get('videoOwnerChannelTitle', None)
    if t["snippet"]["title"] != "Deleted video" and videoOwnerChannelTitle:
        print(
            count,
            ") Title : ",
            t["snippet"]["title"],
            # "\n\tLink : https://www.youtube.com/watch?v=",
            # t["snippet"]["resourceId"]["videoId"],
        )
        video_title = f"{videoOwnerChannelTitle}" + " :: " + t["snippet"]["title"]
        youtube_playlist_titles.append(video_title)

new_songs = False
existing_playlist_titles = None
playlist_name_path = f'youtube_playlist_{PLAYLIST_NAME}'
if os.path.exists(playlist_name_path) and os.path.getsize(playlist_name_path) > 0:
    with open(playlist_name_path, 'r') as f:
        existing_playlist_titles = f.readlines()
    for title in youtube_playlist_titles:
        if title not in existing_playlist_titles:
            new_songs = True
            existing_playlist_titles.insert(0, title)

if new_songs or not os.path.exists(playlist_name_path):
    existing_playlist_titles = '\n'.join(t for t in existing_playlist_titles) if existing_playlist_titles else '\n'.join(t for t in youtube_playlist_titles)
    file_path = root_dir + f"youtube_playlist_{PLAYLIST_NAME}.txt"
    with open(file_path, "w", encoding='utf-8') as outfile:
        outfile.write(existing_playlist_titles)

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'

    with open(file_path, 'rb') as f:
        response = requests.post(url, data={'chat_id': CHAT_ID}, files={'document': f})