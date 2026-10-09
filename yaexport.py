import os
import sys
import json

from dotenv import load_dotenv
from yandex_music import Client

load_dotenv()                      
token = os.getenv("YM_TOKEN")

if not token:
    sys.exit("Нет YM_TOKEN в .env")

client = Client(token).init()     
 
likes = client.users_likes_tracks()
print('Лайкнутых треков:', len(likes.tracks))
tracks = likes.fetch_tracks()


data = []

for track in tracks:
    item ={
        "title": track.title,
        "artists": [a.name for a in track.artists]
    }
    data.append(item)
with open ("likes.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=0, indent=2)
print("Собрано:", len (data))