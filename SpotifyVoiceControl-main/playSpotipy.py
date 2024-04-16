from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint
import webbrowser
import pyautogui
from time import sleep


flag = 0
client_id = "743ede7e2f654ba3894530b1fda46532"
client_secret = "228f1625228e49a3ad5925a2cd6f048d"
autor = ''
song = "In Too Deep".upper()


if len(autor) > 0:

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
    result = sp.search(autor)

    for i in range(0, len(result["tracks"]["items"])):
        name_song = result["tracks"]["items"][i]["name"].upper()
        if song in name_song:
            flag = 1
            webbrowser.open(result["tracks"]["items"][i]["uri"])
            sleep(5)
            pyautogui.press("enter")

if flag == 0:
    song= song.replace(" ", "%20")
    webbrowser.open(f'spotify:search:{song}')
    sleep(5)
    for i in range(28):
        pyautogui.press("tab")
    pyautogui.press("enter")