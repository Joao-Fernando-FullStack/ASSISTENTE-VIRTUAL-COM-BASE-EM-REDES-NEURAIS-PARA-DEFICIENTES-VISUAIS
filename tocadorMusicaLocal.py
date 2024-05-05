import os
import random

import geocoder
import pygame
from nominatim import Nominatim


def tocar_musica(caminho_musica, titulo):
    musicas = os.listdir(caminho_musica)  # Obtém a lista de arquivos no diretório especificado

    # Procura pela música com o título mencionado
    for musica in musicas:
        if titulo.lower() in musica.lower():
            caminho_completo = os.path.join(caminho_musica, musica)
            pygame.mixer.init()

            try:
                pygame.mixer.music.load(caminho_completo)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except pygame.error:
                print("Erro ao reproduzir a música.")


def usd():
    music_dir = "C:/Users/PC/Music"
    songs = os.listdir(music_dir)

    rd = random.choice(songs)
    print(rd)
    os.startfile(os.path.join(music_dir, rd))


import requests

def get_public_ip_address():
    response = requests.get('https://api.ipify.org')
    ip_address = response.text
    return ip_address

print("Seu endereço IP público é:", get_public_ip_address())


import requests

def get_location_from_ip(ip_address):
    response = requests.get(f"https://ipinfo.io/{'105.168.160.141'}/json")
    data = response.json()
    location = data.get("city") + ", " + data.get("region") + ", " + data.get("country")
    return location

# Obter o endereço IP público
def get_public_ip_address():
    response = requests.get('https://api.ipify.org')
    ip_address = response.text
    return ip_address

# Obtém o endereço IP e, em seguida, a localização associada a esse IP
ip_address = get_public_ip_address()
location = get_location_from_ip(ip_address)

print("Sua localização aproximada é:", location)




# Diretório onde suas músicas estão armazenadas
caminho_das_musicas = "C:/Users/PC/Music"

# Captura do título da música digitado pelo usuário
#titulo_musica = input("Digite o título da música: ")

# Toca a música com o título fornecido e o caminho específico
#tocar_musica(caminho_das_musicas, titulo_musica)
#usd()

import requests

def get_location():
    response = requests.get('https://ipapi.co/json/')
    data = response.json()
    city = data.get('city')
    region = data.get('region')
    country = data.get('country_name')
    return f'{city}, {region}, {country}'

print("Sua localização atual é:", get_location())


import pyttsx3

def voice_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Obter a localização geográfica associada ao endereço IP
ip = geocoder.ip("105.168.160.141")
# ip = geocoder.ip("me")  # Use esta linha se quiser obter sua própria localização
latitude, longitude = ip.latlng
la = str(latitude)
lo = str(longitude)

# Reverter as coordenadas de latitude e longitude em um endereço
geolocator = Nominatim(user_agent="geoapiExecises")
location = geolocator.reverse(f"{la},{lo}")
print(location)
voice_speech(f"Não tenho certeza, mas estamos em {location}")






