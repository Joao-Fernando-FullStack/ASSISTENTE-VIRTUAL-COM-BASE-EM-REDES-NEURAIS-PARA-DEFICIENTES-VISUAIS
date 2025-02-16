import datetime
import os
import random
import re
import pygame

import pyttsx3

from mutagen.mp3 import MP3
from mutagen import MutagenError


speech_text = pyttsx3.init()


def voice_speech(text):
    speech_text.setProperty('rate', 220)  # velocidade da fala
    voices = speech_text.getProperty('voices')
    speech_text.setProperty('voices', voices[0].id)  # alterar voz
    speech_text.say(text)
    speech_text.runAndWait()


def enviar_mensagem_whatsapp(numero, mensagem, atraso_segundos=60):
    # Obtém o horário atual
    hora_atual = datetime.datetime.now()
    # Calcula o horário de envio
    hora_envio = hora_atual + datetime.timedelta(seconds=atraso_segundos)
    # Envia a mensagem
    kit.sendwhatmsg(numero, mensagem, hora_envio.hour, hora_envio.minute)


try:
    import pywhatkit as kit
    from urllib.error import URLError
    from AVA.ControladorDispositivo import controladorDispositivoArduino
    from AVA.Functions import latestnews, obter_clima_atual, _hora, _data, greeting_message, \
    speech_recognition, _pesquisar, _lembrete, mostrar_lista_tarefas, adicionar_tarefa, \
    apagar_lista_tarefas, hotword, encerrar, pesquisarWikipedia, piadas, tradutor, sobre
except Exception as ex:
    voice_speech('Desculpe, Para ativar o Assistente Virtual Athena tem que conectar a Internet... Obrigado!')


def validar_mp3(filepath):
    try:
        mp3 = MP3(filepath)
        return True
    except MutagenError:
        return False


def tocarMusica1():
    pygame.mixer.init()
    try:
        music_dir = "C:/Users/PC/Music"
        songs = [song for song in os.listdir(music_dir) if song.endswith('.mp3')]
        random.shuffle(songs)  # Shuffle the list to try different files
        for song in songs:
            song_path = os.path.join(music_dir, song)
            if validar_mp3(song_path):
                try:
                    print(f"Tentando tocar: {song}")
                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play()

                    print(f"Tocando: {song}")
                    break
                except pygame.error as e:
                    print(f"Erro ao tocar {song}: {e}")
                    continue
            else:
                print(f"Arquivo corrompido ou inválido: {song}")
    except Exception as e:
        print(f"Erro ao tocar música: {e}")


def pararMusica():
    pygame.mixer.music.pause()


answer = str()


def voice_command(comando):
    if 'hora' in comando:
        _hora()
    elif 'que dia' in comando:
        _data()
    elif 'clima' in comando:
        obter_clima_atual()
    elif 'terminar' in comando:
        encerrar()
    elif "pesquisar na google" in comando:
        _pesquisar()
    elif "lembrete" in comando:
        _lembrete()
    if "lista de tarefas" in comando:
        mostrar_lista_tarefas()
    elif "adicionar tarefa" in comando:
        adicionar_tarefa()
    elif "apagar tarefa" in comando:
        apagar_lista_tarefas()
    elif "controlar dispositivo" in comando:
        controladorDispositivoArduino()
    elif "tocar música" in comando:
        tocarMusica1()
    elif "para música" in comando:
        pararMusica()
    elif "notícias" in comando:
        latestnews()
    elif "wikipédia" in comando:
        pesquisarWikipedia()
    elif "piadas" in comando:
        piadas()
    elif "tradutor" in comando:
        tradutor()
    elif "quem és" in comando:
        sobre()
    elif "whatsapp" in comando:
        try:
            voice_speech('Diz o número do telefone que desja enviar mensagem!')
            numero = speech_recognition().lower()
            numbers_only = re.sub(r'\D', '', numero)
            voice_speech('Diga a mensagem que deseja enviar')
            mensagem = speech_recognition().lower()
            numbers1 = '+244'+numbers_only
            print(numbers1)
            enviar_mensagem_whatsapp(numbers1, mensagem, atraso_segundos=60)
        except Exception as e:
            print('Erro ao tentar enviar mensagem, verifique o número!')
    else:
        print("comando não válido, diga alguma coisa ou um comando vãlido!")


def acessoAssistente():
    cont = 3
    i = 1
    while cont != 0:
        print('Diga a Hotword para começar...')
        command = speech_recognition().lower()
        if hotword in command:
            greeting_message()
            while answer != 'terminar':
                print('Reconhecimento de voz...')
                command = speech_recognition().lower()
                voice_command(command)
        else:
            i += 1
            print(f'acesso negado! tens agora {cont-1} tentativas')
        cont -= 1


# função principal
if __name__ == '__main__':
    try:
        acessoAssistente()
    except Exception as e:
        print('conectar a Internet!')


