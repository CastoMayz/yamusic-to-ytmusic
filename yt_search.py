import json
from ytmusicapi import YTMusic
from difflib import SequenceMatcher

def same_name(a, b):
    """True, если имена a и b похожи достаточно, чтобы считать их одним исполнителем."""
    a = a.lower().replace(",", "").replace(".", "")
    b = b.lower().replace(",", "").replace(".", "")                              

    if a in b or b in a:                         
        return True

    ratio = SequenceMatcher(None, a, b).ratio()
    return ratio >= 0.85

def artist_matches(ya_artists, result):
    """True, если хотя бы один исполнитель из Яндекса есть в результате YouTube."""
    yt_names = [a["name"] for a in result.get("artists", [])]
    for name in ya_artists:
        if any(same_name(name, yt_name) for yt_name in yt_names):
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