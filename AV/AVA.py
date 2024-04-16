import pyttsx3
import speech_recognition as sr
import requests
import pytz
from datetime import datetime
from babel.dates import format_date, format_time
import webbrowser
import time
import winsound
import sys

from AV.ControladorDispositivo import controladorDispositivoArduino

answer = str()
hotword = 'ativar atena'
speech_text = pyttsx3.init()
hora_atual = datetime.now()
fuso_horario_local = pytz.timezone('Africa/Luanda')
hora_atual_angola = pytz.utc.localize(datetime.now()).astimezone(fuso_horario_local)
cidade = 'Bie'
chave_api = '0431b702a991d8f87c9aa502ac443f11'


def voice_speech(text):
    rate = speech_text.getProperty('rate')
    speech_text.setProperty('rate', 220)  # velocidade da fala
    voices = speech_text.getProperty('voices')
    speech_text.setProperty('voices', voices[1].id)  # alterar voz
    speech_text.say(text)
    speech_text.runAndWait()


def _hora():
    hora = format_time(hora_atual.now(), format='short', locale='pt')
    voice_speech("Agora são: " + hora)


def _data():
    data = format_date(hora_atual.now(), format='full', locale='pt')
    voice_speech(data)


def _lembrete(titulo, hour, minute):
    # Obter o tempo atual
    agora = time.localtime()

    try:
        # Calcular a diferença em segundos até o alarme
        diferenca_segundos = (int(hour) - agora.tm_hour) * 3600 + (int(minute) - agora.tm_min) * 60
        voice_speech(f"Configurado um lembrete para {hour} horas e {minute} minutos com o título {titulo}.")
        # Aguardar até o momento do alarme
        time.sleep(diferenca_segundos)
        # Reproduzir o som de alarme
        winsound.PlaySound('Alarm02.wav', winsound.SND_ALIAS)
    except Exception as e:
        voice_speech("Erro, Intervalo de hora ou minuto não reconhecido... tente novamente!")


def _pesquisar(consulta_pesquisa):
    if consulta_pesquisa:
        url = f"https://www.google.com/search?q={consulta_pesquisa}"
        webbrowser.open(url)
        voice_speech(f"Aqui estão os resultados da pesquisa para {consulta_pesquisa}.")


def greeting_message():
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


def obter_clima_atual(cidade, chave_api):
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

        voice_speech(f"A previsão climática na cidade do Bié, é de, {temperatura:.0f}°C com {descricao}.")
        voice_speech(f"{humidade}%, de humidade.")
        voice_speech(f"pressão atmosférica ,{pressao}, hPa.")
        voice_speech(f"A velocidade do vento, {velocidade_vento}, megabyte por segundo.")
        voice_speech(f"{chuva} Está chovendo.")
    else:
        voice_speech("Não foi possível obter informações sobre o clima.")


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
def adicionar_tarefa(nova_tarefa):
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


def voice_command(comando):
    if 'hora' in comando:
        _hora()
    elif 'dia' in comando:
        _data()
    elif 'clima' in comando:
        obter_clima_atual(cidade, chave_api)

    elif 'termina' in comando:
        voice_speech('Encerrando o programa, Até breve!')
        sys.exit()

    elif "pesquisar na google" in comando:
        voice_speech("O que você gostaria de pesquisar?")
        consulta_pesquisa = speech_recognition()
        _pesquisar(consulta_pesquisa)

    elif "lembrete" in comando:
        voice_speech("Sobre o que você gostaria de ser lembrado?")
        titulo = speech_recognition()
        voice_speech("Diga a hora num intervalo de 0 à 23!")
        hour = speech_recognition()
        voice_speech("Diga os minutos num intervalo de 0 à 59!")
        minute = speech_recognition()
        _lembrete(titulo, hour, minute)

    if "lista de tarefas" in comando:
        mostrar_lista_tarefas()

    elif "adicionar tarefa" in comando:
        voice_speech("Qual tarefa você gostaria de adicionar?")
        nova_tarefa = speech_recognition()
        adicionar_tarefa(nova_tarefa)

    elif "apagar tarefa" in comando:
        apagar_lista_tarefas()

    elif "controlar dispositivo" in comando:
        voice_speech("Diga o comando de voz para o dispositivo que deseja Ligar?")
        command = speech_recognition().lower()
        controladorDispositivoArduino(command)


def main():
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
            voice_speech(f'acesso negado! tens agora {cont-1} tentativas')
        cont -= 1


# função principal
if __name__ == '__main__':
    main()
