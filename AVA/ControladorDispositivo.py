import time
import pyttsx3
import serial
import speech_recognition as sr

speech_text = pyttsx3.init()

# Tenta inicializar a conexão com o Arduino
try:
    import serial
    arduino = serial.Serial('COM5', 9600)  # 'COM5' porta serial do seu Arduino
    arduino_connected = True
except (serial.SerialException, AttributeError):
    arduino_connected = False


def enviar_comando(comando, arduino):
    time.sleep(1.8)  # Aguarda 2 segundos para estabilizar a conexão serial
    arduino.write(comando.encode())


def voice_speech(text):
    speech_text.setProperty('rate', 220)  # velocidade da fala
    voices = speech_text.getProperty('voices')
    speech_text.setProperty('voices', voices[1].id)  # alterar voz
    speech_text.say(text)
    speech_text.runAndWait()


def speech_recognition():
    listener = sr.Recognizer()
    # Recebe informações dita pelo sensor de audio
    with sr.Microphone() as source:
        listener.pause_threshold = 1  # dar pausa para fazer o reconhecimento
        audio = listener.listen(source, timeout=20, phrase_time_limit=40)
        listener.adjust_for_ambient_noise(source)  # Ajusta para o ruído do ambiente
    try:
        # Reconhece o comando apartir de uma Lingua predefinida
        texto = listener.recognize_google(audio, language='pt-BR')
        print("Você disse: " + texto)
        return texto
    except sr.UnknownValueError:
        return "Não entendi o que você disse"
    except sr.RequestError:
        return "Desculpe, ocorreu um erro na minha tentativa de reconhecer sua fala"
    except sr.RequestError as e:
        print(f"Não foi possível solicitar resultados do serviço de reconhecimento de fala do Google; {e}")
        return ""


def controladorDispositivoArduino():
    voice_speech("Diga o comando de voz para o dispositivo que deseja Ligar?")
    comando = speech_recognition().lower()

    try:
        if "desligar lâmpada" in comando:
            enviar_comando('1', arduino)
            print("Desligando a lâmpada...")
            voice_speech("A Lâmpada está desligada!")
        elif "ligar lâmpada" in comando:
            enviar_comando('0', arduino)
            print("Ligando a lâmpada...")
            voice_speech("A Lâmpada está ligada!")
        elif 'desligar ventilador' in comando:
            enviar_comando('3', arduino)
            print("Desligando ventilador...")
            voice_speech("O ventilador está desligado!")
        elif 'ligar ventilador' in comando:
            enviar_comando('2', arduino)
            print("ligando O ventilador...")
            voice_speech("O ventilador está ligado!")
        elif 'desligar dispositivo 3' in comando:
            enviar_comando('5', arduino)
            print("Desligando Dispositivo 3...")
            voice_speech("O Dispositivo 3 está desligado!")
        elif 'ligar dispositivo 3' in comando:
            enviar_comando('4', arduino)
            print("ligando O Dispositivo 3...")
            voice_speech("O Dispositivo 3 está ligado!")
        elif 'desligar dispositivo 4' in comando:
            enviar_comando('7', arduino)
            print("Desligando Dispositivo 4...")
            voice_speech("O Dispositivo 4 está desligado!")
        elif 'ligar dispositivo 4' in comando:
            enviar_comando('6', arduino)
            print("ligando o Dispositivo 4...")
            voice_speech("O Dispositivo 4 está ligado!")
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
        else:
            print("Comando não recoonhecido.")
        arduino.flush()

    except Exception as e:
        voice_speech('O Arduino não está conectado!...')


if __name__ == '__main__':
    # Ligar [0] | Desligar [1]
    enviar_comando('0', arduino)

