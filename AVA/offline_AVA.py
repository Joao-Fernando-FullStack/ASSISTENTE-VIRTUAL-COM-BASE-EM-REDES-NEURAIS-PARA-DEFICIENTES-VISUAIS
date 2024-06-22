import os
import queue
import random
import time
from datetime import datetime

import pygame
from pygame import mixer
import sounddevice as sd
import vosk
import json
import pyttsx3
import requests
import serial
from apscheduler.schedulers.background import BackgroundScheduler
from babel.dates import format_time, format_date
from mutagen.mp3 import MP3
from mutagen import MutagenError


try:
    import serial
    arduino = serial.Serial('COM5', 9600)  # 'COM5' porta serial do seu Arduino
    arduino_connected = True
except (serial.SerialException, AttributeError):
    arduino_connected = False


speech_text = pyttsx3.init()
hora_atual = datetime.now()


def voice_speech(text):
    speech_text.setProperty('rate', 180)  # velocidade da fala ajustada para ser mais clara
    voices = speech_text.getProperty('voices')
    speech_text.setProperty('voice', voices[0].id)  # alterar voz
    speech_text.say(text)
    speech_text.runAndWait()


# Configurações iniciais
MODEL_PATH = "models/vosk-model-small-pt-0.3"
SAMPLE_RATE = 16000
scheduler = BackgroundScheduler()
audio_queue = queue.Queue()

if not os.path.exists(MODEL_PATH):
    print("Por favor, baixe o modelo do Vosk e descompacte-o.")
    exit(1)

model = vosk.Model(MODEL_PATH)


def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))


def get_weather():
    cidade = 'Bie'
    chave_api = '0431b702a991d8f87c9aa502ac443f11'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&units=metric&lang=pt"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados_clima = resposta.json()
        temperatura = dados_clima['main']['temp']
        humidade = dados_clima['main']['humidity']
        pressao = dados_clima['main']['pressure']
        velocidade_vento = dados_clima['wind']['speed']
        descricao = dados_clima['weather'][0]['description']
        chuva = "Sim" if "rain" in descricao else "Não"

        weather_info = (f"A previsão climática na cidade do Bié é de {temperatura:.0f}°C com {descricao}. "
                        f"Humidade de {humidade}%, pressão atmosférica de {pressao} hPa e "
                        f"velocidade do vento de {velocidade_vento} m/s. {chuva} Vai chover? .")
        return weather_info
    else:
        return "Não foi possível obter informações sobre o clima."


def set_reminder(text, time):
    scheduler.add_job(lambda: voice_speech(text), 'date', run_date=time)
    scheduler.start()


def tocarMusica():
    music_dir = "C:/Users/PC/Music"
    songs = os.listdir(music_dir)
    rd = random.choice(songs)
    print(rd)
    os.startfile(os.path.join(music_dir, rd))


def validar_mp3(filepath):
    try:
        mp3 = MP3(filepath)
        return True
    except MutagenError:
        return False

def tocarMusica1():
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



def pausarMusica():
    pygame.mixer.music.pause()


# Função para adicionar uma tarefa à lista
def adicionar_tarefa():
    voice_speech("Qual tarefa você gostaria de adicionar?")
    nova_tarefa = recognize_speech_once()
    try:
        with open("lista_tarefas.txt", "a", encoding="utf-8") as file:
            file.write(f"{nova_tarefa}\n")
        voice_speech(f"Tarefa '{nova_tarefa}' adicionada à lista.")
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")
        voice_speech("Desculpe, ocorreu um erro ao adicionar a tarefa.")


def _hora():
    hora = format_time(hora_atual.now(), format='short', locale='pt')
    voice_speech("Agora são: " + hora)


def _data():
    data = format_date(hora_atual.now(), format='full', locale='pt')
    voice_speech(data)


try:
    import serial
    arduino = serial.Serial('COM5', 9600)  # 'COM5' porta serial do seu Arduino
    arduino_connected = True
except (serial.SerialException, AttributeError):
    arduino_connected = False


def enviar_comando(comando, arduino):
    time.sleep(1.8)  # Aguarda 2 segundos para estabilizar a conexão serial
    arduino.write(comando.encode())

def greeting_message():
    pygame.mixer.init()
    voice_speech('Olá, benvindo de volta! sou sua Assistente Virtual, Athena!')
    hora = int(hora_atual.strftime('%H'))
    if 6 <= hora <= 12:
        voice_speech('Bom dia!')
    elif 12 <= hora <= 18:
        voice_speech('Boa tarde!')
    elif 18 <= hora <= 24:
        voice_speech('Boa noite!')
    else:
        voice_speech('Bom dia!')
    voice_speech('... Estou a sua disposição, diZ-me como posso ajudá-lo!')


# Função para mostrar a lista de tarefas
def mostrar_lista_tarefas():
    try:
        with open("lista_tarefas.txt", "r", encoding="utf-8") as file:
            tarefas = file.readlines()
        if tarefas:
            voice_speech("Aqui está a sua lista de tarefas:")
            for i, tarefa in enumerate(tarefas, 1):
                voice_speech(f"{i}. {tarefa.strip()}")
        else:
            voice_speech("Sua lista de tarefas está vazia.")
    except FileNotFoundError:
        voice_speech("Sua lista de tarefas está vazia.")


# Função para adicionar uma tarefa à lista
def adicionar_tarefa():
    voice_speech("Qual tarefa você gostaria de adicionar?")
    nova_tarefa = recognize_speech_once().lower()
    try:
        with open("lista_tarefas.txt", "a", encoding="utf-8") as file:
            file.write(f"{nova_tarefa}\n")
        voice_speech(f"Tarefa '{nova_tarefa}' adicionada à lista.")
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")
        voice_speech("Desculpe, ocorreu um erro ao adicionar a tarefa.")


# Função para apagar a lista de tarefas
def apagar_lista_tarefas():
    try:
        open("lista_tarefas.txt", "w").close()
        voice_speech("A lista de tarefas foi apagada.")
    except Exception as e:
        print(f"Erro ao apagar a lista de tarefas: {e}")
        voice_speech("Desculpe, ocorreu um erro ao apagar a lista de tarefas.")


def responder(text):
    comando = text.lower()
    if "hora" in comando or "ora" in comando:
        _hora()
    elif "dia" in comando or "bia" in comando:
        _data()
    elif "acender lâmpada" in comando or "acende" in comando:
        enviar_comando('0', arduino)
        print("Ligando a lâmpada...")
        voice_speech("A Lâmpada está ligada!")
    elif "desligar lâmpada" in comando or "desliga" in comando:
        enviar_comando('1', arduino)
        print("Desligando a lâmpada...")
        voice_speech("A Lâmpada está desligada!")
    elif 'desligar ventilador' in comando:
        enviar_comando('3', arduino)
        print("Desligando ventilador...")
        voice_speech("O ventilador está desligado!")
    elif 'ligar ventilador' in comando:
        enviar_comando('2', arduino)
        print("ligando O ventilador...")
        voice_speech("O ventilador está ligado!")
    elif 'desligar tudo' in comando:
        enviar_comando('1', arduino)
        enviar_comando('3', arduino)
        enviar_comando('5', arduino)
        enviar_comando('7', arduino)
        print("desligando o tudo...")
        voice_speech("todos Dispositivos estão desligado!")
    elif 'ligar tudo' in comando:
        enviar_comando('0', arduino)
        enviar_comando('2', arduino)
        enviar_comando('4', arduino)
        enviar_comando('6', arduino)
        print("ligando o tudo...")
        voice_speech("todos Dispositivos estão ligado!")
    if "lista de tarefas" in comando:
        mostrar_lista_tarefas()
    elif "adicionar tarefa" in comando:
        adicionar_tarefa()
    elif "apagar tarefa" in comando:
        apagar_lista_tarefas()
    elif "tocar música" in comando:
        tocarMusica1()
    elif "para" in comando:
        pausarMusica()
    elif "terminar" in comando or "encerra" in comando:
        return True
    else:
        response = "Comando não reconhecido."
        #print(response)
        #voice_speech(response)
    return False


def recognize_speech():
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
        rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        greeting_message()
        print("Reconhecimento de voz, diga algo...")

        while True:
            data = audio_queue.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result_json = json.loads(result)

                print(result_json['text'])
                if responder(result_json["text"]):
                    break
            else:
                partial_result = rec.PartialResult()
                # print(json.loads(partial_result)["partial"])


def recognize_speech_once():
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
        rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        print("Aguardando comando de voz...")

        while True:
            data = audio_queue.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result_json = json.loads(result)
                print(result_json['text'])
                return result_json["text"]
            else:
                partial_result = rec.PartialResult()
                # print(json.loads(partial_result)["partial"])


if __name__ == "__main__":
    try:
        recognize_speech()
    except KeyboardInterrupt:
        print("\nReconhecimento de fala interrompido.")
    except Exception as e:
        print(str(e))

