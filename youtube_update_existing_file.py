import os
import googleapiclient.discovery
import ujson as json
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

NEW_SONGS = 0
EXISTING_PLAYLIST_TITLES = []
PLAYLIST_NAME_PATH = f'youtube_playlist_{PLAYLIST_NAME}.txt'

date = dt.now().strftime("%d-%m-%Y")

# update the working directory
root_dir = os.getcwd() + os.sep

# url = input("Enter youtube playlist id : ")
# query = parse_qs(urlparse(url).query, keep_blank_values=True)
# print(query)
# playlist_id = query["list"][0]


def main():
    print(f"Script starting...")
    print(f"Get all playlist items from playlist '{PLAYLIST_NAME}' | ID:{PLAYLIST_ID}")

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

    FETCHED_PLAYLIST_TITLES = list()

    for number, t in enumerate(playlist_items):
        videoOwnerChannelTitle = t.get('snippet').get('videoOwnerChannelTitle', None)
        if t["snippet"]["title"] != "Deleted video" and videoOwnerChannelTitle:
        # print(
            # number,
            # ") Title : ",
            # t["snippet"]["title"],
            # "\n\tLink : https://www.youtube.com/watch?v=",
            # t["snippet"]["resourceId"]["videoId"],
        # )
            video_title = f"{videoOwnerChannelTitle}" + " :: " + t["snippet"]["title"]
            FETCHED_PLAYLIST_TITLES.append(video_title)

    if os.path.exists(PLAYLIST_NAME_PATH) and os.path.getsize(PLAYLIST_NAME_PATH) > 0:
        with open(PLAYLIST_NAME_PATH, 'r', encoding='utf-8') as f:
            EXISTING_PLAYLIST_TITLES = list(filter(bool, f.read().splitlines()))
        for title in FETCHED_PLAYLIST_TITLES:
            if title not in EXISTING_PLAYLIST_TITLES:
            # print(f'Title: {title} not in {EXISTING_PLAYLIST_TITLES[:10]}')
                NEW_SONGS += 1
                EXISTING_PLAYLIST_TITLES.insert(0, title)

    if NEW_SONGS or not os.path.exists(PLAYLIST_NAME_PATH):
        EXISTING_PLAYLIST_TITLES = '\n'.join(t for t in EXISTING_PLAYLIST_TITLES) if EXISTING_PLAYLIST_TITLES else '\n'.join(t for t in FETCHED_PLAYLIST_TITLES)
        file_path = root_dir + f"youtube_playlist_{PLAYLIST_NAME}.txt"
        with open(file_path, "w", encoding='utf-8') as outfile:
            outfile.write(EXISTING_PLAYLIST_TITLES)

        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'

        text = f"Playlist `{PLAYLIST_NAME}` was successfully fetched!"
        text_updated = f"Playlist `{PLAYLIST_NAME}` was successfully updated with {NEW_SONGS} new songs!\n\n#youtubeplaylist"
        print(text_updated if NEW_SONGS else text)

        data = {'chat_id': CHAT_ID, 'caption': text_updated if NEW_SONGS else text}

        with open(file_path, 'rb') as f:
            response = requests.post(url, data=data, files={'document': f})


if __name__ == "__main__":
    main()


