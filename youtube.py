import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import json
from datetime import datetime as dt
import os

from dotenv import load_dotenv

load_dotenv()

DEV_KEY = os.getenv('DEV_KEY')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')
PLAYLIST_NAME = os.getenv('PLAYLIST_NAME', '1')

date = dt.now().strftime("%d-%m-%Y")

# update the working directory
root_dir = os.getcwd() + os.sep



# url = input("Enter youtube playlist id : ")
# query = parse_qs(urlparse(url).query, keep_blank_values=True)
# print(query)
# PLAYLIST_ID = query["list"][0]

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

youtube_playlist = dict()
video_list = list()

for t in playlist_items:
    if t["snippet"]["title"] != "Deleted video":
        print(
            count,
            ") Title : ",
            t["snippet"]["title"],
            "\n\tLink : https://www.youtube.com/watch?v=",
            t["snippet"]["resourceId"]["videoId"],
        )
        video_dict = dict()
        video_dict["video_number"] = count
        video_dict["title"] = t["snippet"]["title"]
        video_dict["link"] = (
            "https://www.youtube.com/watch?v=" + t["snippet"]["resourceId"]["videoId"]
        )
        video_list.append(video_dict)
        count += 1

youtube_playlist["video_list"] = video_list
youtube_playlist["total_videos"] = count

json_object = json.dumps(youtube_playlist, ensure_ascii=False, indent=4)

with open(root_dir + f"youtube_playlist_{PLAYLIST_NAME}_{date}.json", "w", encoding='utf-8') as outfile:
    outfile.write(json_object)

print("Json file dump completed...")

youtube_playlist_titles = list()

for t in playlist_items:
    if t["snippet"]["title"] != "Deleted video":
        # print(
        #     count,
        #     ") Title : ",
        #     t["snippet"]["title"],
        #     "\n\tLink : https://www.youtube.com/watch?v=",
        #     t["snippet"]["resourceId"]["videoId"],
        # )

        video_title = t["snippet"]["title"]

        youtube_playlist_titles.append(video_title)

youtube_playlist_titles = '\n'.join(t for t in youtube_playlist_titles)

with open(root_dir + f"youtube_playlist_{PLAYLIST_NAME}_{date}.txt", "w", encoding='utf-8') as outfile:
    
    outfile.write(youtube_playlist_titles)
