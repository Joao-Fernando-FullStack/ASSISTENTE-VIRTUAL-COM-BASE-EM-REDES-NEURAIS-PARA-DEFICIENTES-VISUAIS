import os
import queue
import sounddevice as sd
import vosk
import json
import pyttsx3
from datetime import datetime, timedelta
import requests
import serial
from apscheduler.schedulers.background import BackgroundScheduler

# Configurações iniciais
MODEL_PATH = "../models/vosk-model-pt-fb-v0.1.1-20220516_2113"
SAMPLE_RATE = 16000
engine = pyttsx3.init()
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

def get_weather(city):
    api_key = "YOUR_API_KEY"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]['description']
        temperature = main['temp']
        return f"A temperatura em {city} é {temperature} graus Celsius com {weather}."
    else:
        return "Não consegui obter a previsão do tempo para essa cidade."

def control_arduino(command):
    ser = serial.Serial('COM3', 9600)  # Substitua 'COM3' pela porta correta
    ser.write(command.encode())
    ser.close()

def set_reminder(text, time):
    scheduler.add_job(lambda: engine.say(text) and engine.runAndWait(), 'date', run_date=time)
    scheduler.start()

def respond(text):
    if "que horas são" in text.lower() or "que horas sao" in text.lower():
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        response = f"Agora são {current_time}"
        print(response)
        engine.say(response)
        engine.runAndWait()
    elif "previsão do tempo" in text.lower():
        city = text.split("em")[-1].strip()
        weather_info = get_weather(city)
        print(weather_info)
        engine.say(weather_info)
        engine.runAndWait()
    elif "ligar lâmpada" in text.lower() or "ligar lampada" in text.lower():
        control_arduino("LIGAR_LAMPADA")
        response = "Lâmpada ligada."
        print(response)
        engine.say(response)
        engine.runAndWait()
    elif "desligar lâmpada" in text.lower() or "desligar lampada" in text.lower():
        control_arduino("DESLIGAR_LAMPADA")
        response = "Lâmpada desligada."
        print(response)
        engine.say(response)
        engine.runAndWait()
    elif "lembrar de" in text.lower():
        parts = text.split("lembrar de")
        reminder_text = parts[1].strip()
        if "em" in reminder_text:
            parts = reminder_text.split("em")
            reminder_text = parts[0].strip()
            time_part = parts[1].strip()
            reminder_time = datetime.strptime(time_part, "%H:%M")
            now = datetime.now()
            reminder_time = now.replace(hour=reminder_time.hour, minute=reminder_time.minute, second=0, microsecond=0)
            set_reminder(reminder_text, reminder_time)
            response = f"Lembrete definido para: {reminder_text} às {time_part}"
            print(response)
            engine.say(response)
            engine.runAndWait()
        else:
            response = "Por favor, forneça a hora do lembrete no formato correto."
            print(response)
            engine.say(response)
            engine.runAndWait()
    else:
        print("Comando não reconhecido.")
        engine.say("Comando não reconhecido.")
        engine.runAndWait()

def recognize_speech():
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        print("Diga algo...")

        while True:
            data = audio_queue.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result_json = json.loads(result)
                print(result_json["text"])
                respond(result_json["text"])
            else:
                partial_result = rec.PartialResult()
                print(json.loads(partial_result)["partial"])

if __name__ == "__main__":
    try:
        recognize_speech()
    except KeyboardInterrupt:
        print("\nReconhecimento de fala interrompido.")
    except Exception as e:
        print(str(e))
