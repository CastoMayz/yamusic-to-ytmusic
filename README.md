# yamusic-to-ytmusic

Перенос библиотеки песен из Яндекс музыки в Youtube Music с последующим прослушиванием

## Зачем

Часть треков в Яндекс музыке стала недоступна, решил попробовать другую площадку, а заодно - разобраться с API.

## Как работает

1. yaexport.py выгружает библиотеку яндекса, сохраняя её в likes.json.
2. yt_search.py находит соответствия между названием песни из яндекс музыки, сравнивая с найденными результатами в youtube. ищет по исполнителю, названию и версии, затем проверяет исполнителя: сначала точное совпадение, потом похожее.
3. то, что не удалось найти - уходит в suspicious.json
4. Импорт библиотеки в Youtube Music (в разработке)

## Установка и запуск

Для поиска нужен доступ к YouTube.

```
git clone https://github.com/CastoMayz/yamusic-to-ytmusic.git
cd yamusic-to-ytmusic
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Получить токен Яндекс Музыки (откроется ссылка, на ней нужно ввести код):

```
python get_token.py
```

Создать файл `.env` и записать в него токен:

```
YM_TOKEN=ваш_access_token
```

Запуск:

```
python yaexport.py     # выгрузка лайков в likes.json
python yt_search.py    # поиск в YouTube Music → matches.json и suspicious.json
```

## Статус

Выгрузка библиотеки из ЯМ, Поиск соответствий в Youtube. автоматически находится 167 из 181 трека. Импорт - в разработке.