import os
import random
import datetime
import pywhatkit as kit
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
from wikipedia import wikipedia
from deep_translator import GoogleTranslator
from pyjokes import pyjokes


hotword = 'ativar assistente'
speech_text = pyttsx3.init()
hora_atual = datetime.now()
fuso_horario_local = pytz.timezone('Africa/Luanda')
hora_atual_angola = pytz.utc.localize(datetime.now()).astimezone(fuso_horario_local)


def _hora():
    hora = format_time(hora_atual.now(), format='short', locale='pt')
    voice_speech("Agora são: " + hora)


def _data():
    data = format_date(hora_atual.now(), format='full', locale='pt')
    voice_speech(data)


def _lembrete():
    # Obter o tempo atual
    agora = time.localtime()
    voice_speech("Sobre o que você gostaria de ser lembrado?")
    titulo = speech_recognition()
    voice_speech("Diga a hora num intervalo de 0 à 23!")
    hour = speech_recognition()
    voice_speech("Diga os minutos num intervalo de 0 à 59!")
    minute = speech_recognition()

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


def _pesquisar():
    voice_speech("O que você gostaria de pesquisar?")
    consulta_pesquisa = speech_recognition().lower()
    if consulta_pesquisa:
        url = f"https://www.google.com/search?q={consulta_pesquisa}"
        webbrowser.open(url)
        voice_speech(f"Aqui estão os resultados da pesquisa para {consulta_pesquisa}.")





def greeting_message():
    voice_speech('Olá, benvindo de volta!')
    hora = int(hora_atual.strftime('%H'))
    if 6 <= hora <= 12:
        voice_speech('Bom dia!')
    elif 12 <= hora <= 18:
        voice_speech('Boa tarde!')
    elif 18 <= hora <= 24:
        voice_speech('Boa noite!')
    else:
        voice_speech('Bom dia!')
    voice_speech('... Estou a sua disposição, como posso ajudá-lo!')


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
    nova_tarefa = speech_recognition().lower()
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
    try:
        listener = sr.Recognizer()
        # Recebe informações dita pelo sensor de audio
        with sr.Microphone() as source:
            listener.pause_threshold = 1  # dar pausa para fazer o reconhecimento
            audio = listener.listen(source, timeout=20, phrase_time_limit=40)
            listener.adjust_for_ambient_noise(source)  # Ajusta para o ruído do ambiente
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


def voice_speech(text):
    speech_text.setProperty('rate', 220)  # velocidade da fala
    voices = speech_text.getProperty('voices')
    speech_text.setProperty('voices', voices[1].id)  # alterar voz
    speech_text.say(text)
    speech_text.runAndWait()


def voice_speech1(text):
    speech_text.setProperty('rate', 150)  # velocidade da fala
    voices = speech_text.getProperty('voices')
    speech_text.setProperty('voices', voices[1].id)  # alterar voz
    speech_text.say(text)
    speech_text.runAndWait()


def latestnews():
    pais = 'pt'
    api_dict = {"negócios" : f"https://newsapi.org/v2/top-headlines?country={pais}&category=business&apiKey"
                             f"=5b82b45932bd4045a6069a2e0b86b4b6&lang=pt",
                "entretenimento" : f"https://newsapi.org/v2/top-headlines?country={pais}&category=entertainment"
                                   f"&apiKey=5b82b45932bd4045a6069a2e0b86b4b6&lang=pt",
                "ciência" : f"https://newsapi.org/v2/top-headlines?country={pais}&category=science&apiKey"
                            f"=5b82b45932bd4045a6069a2e0b86b4b6&lang=pt",
                "esportes" : f"https://newsapi.org/v2/top-headlines?country={pais}&category=sports&apiKey"
                             f"=5b82b45932bd4045a6069a2e0b86b4b6&lang=pt",
                "tecnologia" : f"https://newsapi.org/v2/top-headlines?country={pais}&category=technology&apiKey"
                               f"=5b82b45932bd4045a6069a2e0b86b4b6&lang=pt"
    }

    url = None
    voice_speech("De qual área você deseja notícias? Negócios, entretenimento, ciência, esportes ou tecnologia?")
    voice_speech("Diz a área de notícias que você deseja? ")
    field = speech_recognition().lower()
    for key, value in api_dict.items():
        if key.lower() in field.lower():
            url = value
            print(url)
            voice_speech("URL encontrada")
            break
    if url is None:
        #voice_speech("URL não encontrada")
        return

    news = requests.get(url).json()
    voice_speech("Aqui está a primeira notícia.")
    articles = news["articles"]
    for article in articles:
        title = article["title"]
        print(title)
        voice_speech(title)
        news_url = article["url"]
        print(f"Para mais informações, visite: {news_url}")

        voice_speech("[Diga 1 para continuar e 2 para parar]:")
        choice = speech_recognition().lower()
        if choice == "2":
            break
    voice_speech("Isso é tudo por agora.")


def obter_clima_atual():
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

        voice_speech(f"A previsão climática na cidade do Bié, é de, {temperatura:.0f}°C com {descricao}.")
        voice_speech(f"{humidade}%, de humidade.")
        voice_speech(f"pressão atmosférica ,{pressao}, hPa.")
        voice_speech(f"A velocidade do vento, {velocidade_vento}, megabyte por segundo.")
        voice_speech(f"{chuva} irá chover.")
    else:
        voice_speech("Não foi possível obter informações sobre o clima.")


def pesquisarWikipedia():
    try:
        voice_speech("Diga o tema que deseja saber?...")
        topic = speech_recognition().lower()
        wikipedia.set_lang('pt')
        result = wikipedia.summary(topic, sentences=2)
        print(result)
        voice_speech("de acordo a wikipedia")
        voice_speech(result)
    except Exception as e:
        voice_speech('Desculpe, não consegui encontrar informações sobre esse tópico')


def tocarMusica():
    music_dir = "C:/Users/PC/Music"
    songs = os.listdir(music_dir)
    rd = random.choice(songs)
    print(rd)
    os.startfile(os.path.join(music_dir, rd))


def piadas():
    tradutor = GoogleTranslator(source="en", target="pt")
    joke = pyjokes.get_joke()
    texto = joke
    traducao = tradutor.translate(texto)
    voice_speech1(traducao)


def tradutor():
    voice_speech('Que frase deseja traduzir em Ingles?')
    comando = speech_recognition().lower()
    tradutor = GoogleTranslator(source="pt", target="en")
    traducao = tradutor.translate(comando)
    voice_speech1(traducao)


def encerrar():
    voice_speech('Encerrando o programa, Até breve!')
    sys.exit()


def ajuda():
    voice_speech("Seja benvindo ao menu de ajuda")
    voice_speech("Para saber a hora diga 1")
    voice_speech("Para saber o dia diga 2")
    voice_speech("Para saber a previsão do clima diga 3")
    voice_speech("Para tocar música diga 4")


def sobre():
    voice_speech("Sou a assistente virtual Athena, desenvolvido por João, Fernando, Matias. Em 2023.")
    voice_speech("Fui desenvolvido para ajudar você,em suas atividades diárias.")

