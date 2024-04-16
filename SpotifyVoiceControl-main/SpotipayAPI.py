import speech_recognition as sr
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import pyttsx3
import os 

listener = sr.Recognizer()

sr.Microphone.list_microphone_names()

def ouvir():
    try:
        with sr.Microphone(device_index=1) as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice,language='pt-PT')
            print(command)
            return command
    except:
        return 'No Sound'

os.environ['SPOTIPY_CLIENT_ID'] = '743ede7e2f654ba3894530b1fda46532'
os.environ['SPOTIPY_CLIENT_SECRET'] = '228f1625228e49a3ad5925a2cd6f048d'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com/callback'

client_id = "743ede7e2f654ba3894530b1fda46532"
client_secret = "228f1625228e49a3ad5925a2cd6f048d"

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

engine = pyttsx3.init()
engine.say('This is a new test message!')
engine.runAndWait()

while True:
    command = ouvir()

    if 'spotify play' in command.lower():
        query = command.lower().replace('spotify play','').strip()

        results = sp.search(query,1,0,"track")

        nome_artista = results['tracks']['items'][0]['artists'][0]['name']
        nome_musica = results['tracks']['items'][0]['name']
        track_uri = results['tracks']['items'][0]['uri']

        engine.say(f'Playing {nome_musica} by {nome_artista}')
        engine.runAndWait()

        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
        result = sp.search(nome_artista)

        sp.start_playback(uris=[track_uri])

    elif 'spotify pause' in command.lower():
        sp.pause_playback()
    elif 'spotify continue' in command.lower():
        sp.start_playback()
    elif 'spotify change volume to' in command.lower():
        volume = int(command.lower().replace('spotify change volume to','').strip())
        sp.volume(volume)


















