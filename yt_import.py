import sys
import json
from ytmusicapi import YTMusic

PLAYLIST_TITLE = "Из Яндекс Музыки"

yt = YTMusic("browser.json")

with open("matches.json", "r", encoding="utf-8") as file:
    matches = json.load(file)

#Собираем videoId найденных треков, повторы убираем (порядок сохраняется)
video_ids = list(dict.fromkeys(m["videoId"] for m in matches))

#Пробный запуск: python yt_import.py --test — только первые 3 трека
if "--test" in sys.argv:
    video_ids = video_ids[:3]

print("Треков к переносу:", len(video_ids))

playlist_id = yt.create_playlist(
    PLAYLIST_TITLE,
    "Перенесено из Яндекс Музыки скриптом yamusic-to-ytmusic",
    privacy_status="PRIVATE",
    video_ids=video_ids,
)

#При успехе create_playlist возвращает id плейлиста (строку), при ошибке — ответ сервера
if not isinstance(playlist_id, str):
    sys.exit(f"Не удалось создать плейлист: {playlist_id}")

print("Готово:", f"https://music.youtube.com/playlist?list={playlist_id}")
