import time
import pyttsx3
import serial

engine = pyttsx3.init()
engine.setProperty('rate', 220)  # Ajusta a velocidade da fala


def enviar_comando(comando, arduin):
    arduin.write(comando.encode())


def falar(audio):
    engine.setProperty('rate', 220)  #velocidade
    voices = engine.getProperty('voices')
    engine.setProperty('voices',voices[1].id) #alterar voz
    engine.say(audio)
    engine.runAndWait()


def controladorDispositivoArduino(comando):
    try:
        arduino = serial.Serial('COM5', 9600)  # 'COM5' porta serial do seu Arduino
        time.sleep(2)  # Aguarda 2 segundos para estabilizar a conexão serial
    except Exception as e:
        print('Arduino não conectado!')


    if "desligar lâmpada" in comando:
        enviar_comando('1', arduino)
        print("Desligando a lâmpada...")
        falar("A Lâmpada está desligada!")
    elif "ligar lâmpada" in comando:
        enviar_comando('0', arduino)
        print("Ligando a lâmpada...")
        falar("A Lâmpada está ligada!")
    elif 'desligar dispositivo 2' in comando:
        enviar_comando('3', arduino)
        print("Desligando Dispositivo 2...")
        falar("O Dispositivo 2 está desligado!")
    elif 'ligar dispositivo 2' in comando:
        enviar_comando('2', arduino)
        print("ligando O Dispositivo 2...")
        falar("O Dispositivo 2 está ligado!")
    elif 'desligar dispositivo 3' in comando:
        enviar_comando('5', arduino)
        print("Desligando Dispositivo 3...")
        falar("O Dispositivo 3 está desligado!")
    elif 'ligar dispositivo 3' in comando:
        enviar_comando('4', arduino)
        print("ligando O Dispositivo 3...")
        falar("O Dispositivo 3 está ligado!")
    elif 'desligar dispositivo 4' in comando:
        enviar_comando('7', arduino)
        print("Desligando Dispositivo 4...")
        falar("O Dispositivo 4 está desligado!")
    elif 'ligar dispositivo 4' in comando:
        enviar_comando('6', arduino)
        print("Desligando o Dispositivo 4...")
        falar("O Dispositivo 4 está ligado!")
    else:
        print("Comando não reconhecido.")
    arduino.flush()

if __name__ == '__main__':
    # controladorDispositivoArduino('desligar lâmpada')

