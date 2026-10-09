import json
from ytmusicapi import YTMusic
from difflib import SequenceMatcher

SequenceMatcher(None, "dj zup raiii", "dj zup ralii").ratio()   # МЫ ЗДЕСЬ, ДЕЛАЕМ СРАВНЕНИЕ ИМЕНИ
def artist_matches(ya_artists, result):
    """True, если хотя бы один исполнитель из Яндекса есть в результате YouTube."""
    yt_names = [a["name"].lower() for a in result.get("artists", [])]
    for name in ya_artists:
        if name.lower() in yt_names:
            return True
    return False

yt = YTMusic()
with open ("likes.json", "r", encoding="utf-8") as file:
    data = json.load(file)
matches = []
suspicious = []

for track in data:
    ya_artists = " ".join(track["artists"])
    query = f"{ya_artists} {track['title']}"
    results = yt.search(query, filter="songs")

    best = None
    for r in results[:5]:                  # первые 5 результатов
        if artist_matches(track["artists"], r):
            best = r
            break                          # нашли — дальше не ищем

    if best is None:
        print("ПРОВЕРИТЬ:", query)
        suspicious.append(query)
        continue

    yt_artists = ", ".join([a["name"] for a in best.get("artists", [])])
    found = f"{yt_artists} - {best["title"]}"            
    print(query, "→", found)

    matches.append({
        "query": query,
        "found": found,
        "videoId": best["videoId"],
    })
with open("matches.json", "w", encoding="utf-8") as file:
    json.dump(matches, file, ensure_ascii=False, indent=2)
with open("suspicious.json", "w", encoding="utf-8") as file:
    json.dump(suspicious, file, ensure_ascii=False, indent=2)
print("Найдено:", len(matches), "из", len(data))