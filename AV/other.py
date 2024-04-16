import locale

import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import time
import threading


#locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')

# Inicializa o mecanismo de texto para fala
engine = pyttsx3.init()

# Função para converter texto em fala
def falar(texto):
    engine.say(texto)
    engine.runAndWait()

# Função para reconhecer a fala
def reconhecer_fala():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        falar("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Reconhecendo...")
        comando = recognizer.recognize_google(audio, language="pt-BR").lower()
        print(f"Usuário: {comando}")
        return comando
    except sr.UnknownValueError:
        print("Desculpe, não consegui entender o áudio.")
        return ""
    except sr.RequestError as e:
        print(f"Não foi possível solicitar resultados do serviço de reconhecimento de fala do Google; {e}")
        return ""

# Função para realizar ações com base nos comandos do usuário
def realizar_acao(comando):
    if "lista de tarefas" in comando:
        mostrar_lista_tarefas()

    elif "adicionar tarefa" in comando:
        falar("Qual tarefa você gostaria de adicionar?")
        nova_tarefa = reconhecer_fala()
        adicionar_tarefa(nova_tarefa)

    elif "apagar tarefa" in comando:
        apagar_lista_tarefas()

    elif "adicionar lembrete" in comando:
        falar("Sobre o que você gostaria de ser lembrado?")
        assunto_lembrete = reconhecer_fala()
        falar("Quando você gostaria de ser lembrado? Por exemplo, diga 'amanhã às 15 horas'")
        horario_lembrete = reconhecer_fala()
        agendar_lembrete2(assunto_lembrete, horario_lembrete)

    elif "listar lembrete" in comando:
        #mostrar_lista_tarefas();
        mostrar_lembretes_agendados();

    elif "apagar lembrete" in comando:
        falar("Qual é o assunto do lembrete que deseja apagar?")
        assunto = reconhecer_fala()
        apagar_lembrete(assunto)

    elif "apagar todos lembrete" in comando:
        #falar("Qual é o assunto do lembrete que deseja apagar?")
       # assunto = reconhecer_fala()
        apagar_todos_os_lembretes()


    # ... (outras implementações de comandos)

# Função para mostrar a lista de tarefas
def mostrar_lista_tarefas():
    try:
        with open("lista_tarefas.txt", "r", encoding="utf-8") as file:
            tarefas = file.readlines()
        if tarefas:
            falar("Aqui está a sua lista de tarefas:")
            for i, tarefa in enumerate(tarefas, 1):
                falar(f"{i}. {tarefa.strip()}")
        else:
            falar("Sua lista de tarefas está vazia.")
    except FileNotFoundError:
        falar("Sua lista de tarefas está vazia.")

# Função para adicionar uma tarefa à lista
def adicionar_tarefa(nova_tarefa):
    try:
        with open("lista_tarefas.txt", "a", encoding="utf-8") as file:
            file.write(f"{nova_tarefa}\n")
        falar(f"Tarefa '{nova_tarefa}' adicionada à lista.")
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")
        falar("Desculpe, ocorreu um erro ao adicionar a tarefa.")


# Função para apagar a lista de tarefas
def apagar_lista_tarefas():
    try:
        open("lista_tarefas.txt", "w").close()
        falar("A lista de tarefas foi apagada.")
    except Exception as e:
        print(f"Erro ao apagar a lista de tarefas: {e}")
        falar("Desculpe, ocorreu um erro ao apagar a lista de tarefas.")


# Função para agendar um lembrete
# Função para agendar um lembrete
import dateutil.parser

# Função para agendar um lembrete
def agendar_lembrete2(assunto, horario):
    try:
        agora = datetime.datetime.now()
        horario_parsed = dateutil.parser.parse(horario, fuzzy=True)

        # Se o horário fornecido não incluir uma hora, assumimos 15:00
        if horario_parsed.hour == 0 and horario_parsed.minute == 0 and horario_parsed.second == 0:
            horario_parsed = horario_parsed.replace(hour=15, minute=0, second=0)

        with open("lembretes.txt", "a", encoding="utf-8") as file:
            file.write(f"{assunto} em {horario_parsed}\n")

        horario_formatado = horario_parsed.strftime("%A, %d de %m de %Y às %H:%M").capitalize()
        falar(f"Lembrete para '{assunto}' agendado para {horario_formatado}.")
        print(horario_parsed)
        print(horario_formatado)
        # Iniciar uma thread para verificar periodicamente os lembretes
        threading.Thread(target=verificar_lembretes).start()

    except Exception as e:
        print(f"Erro ao agendar lembrete: {e}")
        falar("Desculpe, ocorreu um erro ao agendar o lembrete.")



def apagar_todos_os_lembretes():
    try:
        open("lembretes.txt", "w").close()
        falar("Todos os lembretes foram apagados.")
    except Exception as e:
        print(f"Erro ao apagar todos os lembretes: {e}")
        falar("Desculpe, ocorreu um erro ao apagar todos os lembretes.")


def apagar_lembrete(assunto):
    try:
        with open("lembretes.txt", "r", encoding="utf-8") as file:
            lembretes = file.readlines()

        lembrete_encontrado = False
        novos_lembretes = []

        for lembrete in lembretes:
            if assunto.lower() in lembrete.lower():
                lembrete_encontrado = True
                falar(f"Lembrete sobre '{assunto}' apagado.")
            else:
                novos_lembretes.append(lembrete)

        if not lembrete_encontrado:
            falar(f"Lembrete sobre '{assunto}' não encontrado.")

        with open("lembretes.txt", "w", encoding="utf-8") as file:
            file.writelines(novos_lembretes)

    except Exception as e:
        print(f"Erro ao apagar lembrete: {e}")
        falar("Desculpe, ocorreu um erro ao apagar o lembrete.")


def agendar_lembrete1(assunto, horario):
    try:
        agora = datetime.datetime.now()

        if "hoje" in horario:
            horario_hoje = agora.replace(hour=15, minute=0, second=0)
            with open("lembretes.txt", "a", encoding="utf-8") as file:
                file.write(f"{assunto} em {horario_hoje}\n")
            falar(f"Lembrete para '{assunto}' agendado para hoje às 15:00.")
            # Iniciar uma thread para verificar periodicamente os lembretes
            threading.Thread(target=verificar_lembretes).start()

        elif "amanhã" in horario:
            horario_amanha = agora + datetime.timedelta(days=1)
            horario_amanha = horario_amanha.replace(hour=horario, minute=0, second=0)
            with open("lembretes.txt", "a", encoding="utf-8") as file:
                file.write(f"{assunto} em {horario_amanha}\n")
            falar(f"Lembrete para '{assunto}' agendado para amanhã às 15:00.")
            # Iniciar uma thread para verificar periodicamente os lembretes
            threading.Thread(target=verificar_lembretes).start()

        else:
            falar("Desculpe, o formato do horário não é suportado neste exemplo.")

    except Exception as e:
        print(f"Erro ao agendar lembrete: {e}")
        falar("Desculpe, ocorreu um erro ao agendar o lembrete.")

def agendar_lembrete(assunto, horario):
    try:
        horario_formatado = datetime.datetime.strptime(horario, "%Y-%m-%d %H:%M:%S")
        with open("lembretes.txt", "a", encoding="utf-8") as file:
            file.write(f"{assunto} em {horario_formatado}\n")
        falar(f"Lembrete para '{assunto}' agendado para {horario_formatado}.")
        # Iniciar uma thread para verificar periodicamente os lembretes
        threading.Thread(target=verificar_lembretes).start()
    except Exception as e:
        print(f"Erro ao agendar lembrete: {e}")
        falar("Desculpe, ocorreu um erro ao agendar o lembrete.")

def mostrar_lembretes_agendados():
    try:
        with open("lembretes.txt", "r", encoding="utf-8") as file:
            lembretes = file.readlines()
        if lembretes:
            falar("Aqui estão os lembretes agendados:")
            for lembrete in lembretes:
                falar(lembrete.strip())
        else:
            falar("Não há lembretes agendados.")
    except FileNotFoundError:
        falar("Não há lembretes agendados.")

# Função para verificar e anunciar lembretes
def verificar_lembretes():
    while True:
        try:
            with open("lembretes.txt", "r", encoding="utf-8") as file:
                lembretes = file.readlines()
            agora = datetime.datetime.now()
            for lembrete in lembretes:
                partes = lembrete.split(" em ")
                assunto = partes[0].strip()
                horario_formatado = datetime.datetime.strptime(partes[1].strip(), "%Y-%m-%d %H:%M:%S")
                if agora >= horario_formatado:
                    falar(f"Lembrete: {assunto}.")
                    # Remover lembrete após anunciá-lo
                    lembretes.remove(lembrete)
                    with open("lembretes.txt", "w", encoding="utf-8") as file:
                        file.writelines(lembretes)
        except FileNotFoundError:
            pass
        time.sleep(60)  # Verificar lembretes a cada minuto

# Loop principal para o assistente de voz
while True:
    falar("Como posso ajudar?")
    comando_usuario = reconhecer_fala()
    realizar_acao(comando_usuario)
