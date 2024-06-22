import os
import random
import pygame
from mutagen.mp3 import MP3
from mutagen import MutagenError

# Inicializa o mixer do pygame
pygame.mixer.init()

def tocarMusica():
    music_dir = "C:/Users/PC/Music"
    songs = os.listdir(music_dir)
    rd = random.choice(songs)
    print(f"Tocando: {rd}")
    pygame.mixer.music.load(os.path.join(music_dir, rd))
    pygame.mixer.music.play()

def pausarMusica():
    pygame.mixer.music.pause()

def retomarMusica():
    pygame.mixer.music.unpause()

# Exemplo de uso
tocarMusica()

# Aguarde um tempo antes de pausar a música (10 segundos neste caso)
import time
time.sleep(10)
pausarMusica()

# Aguarde um tempo antes de retomar a música (5 segundos neste caso)
time.sleep(5)
retomarMusica()


