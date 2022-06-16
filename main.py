import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

load_dotenv("C:/Users/hanna/OneDrive/Documents/Learning/EnvironmentVariables/.env")
pp = pprint.PrettyPrinter(indent=4)


date = input("What year do you want to travel to? Type the date in the following format: \n")
# date = "2000-01-20"
billboard_endpoint = "https://www.billboard.com/charts/hot-100/" + date + "/"
response = requests.get(billboard_endpoint)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
# print(soup.prettify())

song_title_tags = soup.select(selector="li ul li h3")
song_titles = [item.text.strip() for item in song_title_tags]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                               client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                               redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                                               scope="playlist-modify-private",
                                               cache_path="token.txt"))
user = sp.current_user()["id"]

uris = []
for title in range(100):
    track = song_titles[title]
    try:
        search_result = sp.search(q=f"track: {track} year: 2000")["tracks"]["items"][0]["uri"]
        uris.append(search_result)
    except IndexError:
        continue

playlist = sp.user_playlist_create(user=user, name=f"{date} Billboard 100", public=False)['id']

print(sp.playlist_add_items(playlist_id=playlist, items=uris))
