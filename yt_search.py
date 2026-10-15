import json
from ytmusicapi import YTMusic
from difflib import SequenceMatcher

def same_duration (ym, yt):
    tolerance=3
    if yt is None or ym is None:
        return True
    return abs(yt-ym)<=tolerance
  

#Сравнение имени из яндекс музыки и полученного результата
def same_name(a, b):                                                                    
    """True, если имена a и b похожи достаточно, чтобы считать их одним исполнителем."""
    a = a.lower().replace(",", "").replace(".", "")
    b = b.lower().replace(",", "").replace(".", "")                              

    if a in b or b in a:                         
        return True

    ratio = SequenceMatcher(None, a, b).ratio()
    return ratio >= 0.85

#Сравнение исполнителя/ей, смотря что передали в exact - точное или похожее
def artist_matches(ya_artists, result, exact):                                        
    """True, если исполнитель из Яндекса совпадает с исполнителем результата YouTube.
    exact=True — строгое сравнение (без учёта регистра), exact=False — нечёткое через same_name."""
    yt_names = [a["name"] for a in result.get("artists", [])]
    for name in ya_artists:
        for yt_name in yt_names:
            if exact and name.lower() == yt_name.lower():
                return True
            if not exact and same_name(name, yt_name):
                return True
    return False

#Сравнение 5 первых результатов - сначала ищет точное совпадение, потом примерное. если не нашло - ничего
def find_best(results, track):
    """Лучший результат поиска для трека из Яндекса или None."""
    top = results[:5]

    for r in top:
        if artist_matches(track["artists"], r, exact=True) and same_name(track["title"], r.get("title")) and same_duration(track["duration"], r.get("duration_seconds")):    # точно
            return r

    for r in top:
        if artist_matches(track["artists"], r, exact=False) and same_name(track["title"], r.get("title")) and same_duration(track["duration"], r.get("duration_seconds")):   # похоже
            return r

    return None

yt = YTMusic() 
with open ("likes.json", "r", encoding="utf-8") as file:
    data = json.load(file)
matches = []
suspicious = []
#Поиск трека по данным из библиотеки яндекс, дальше - сравнение. не подходит - отправляем в проверить. 
for track in data:
    ya_artists = " ".join(track["artists"])
    query = f"{ya_artists} {track['title']}"
    if track.get("version"):
        query += " " + track["version"]
    query = query.replace(" -", " ")
    results = yt.search(query, filter="songs")

    best = find_best(results, track)                      

    if best is None:
        print("ПРОВЕРИТЬ:", query)
        suspicious.append(query)
        continue
    #Записываем полученные данные из ютуб музыки, добавляя в matches
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