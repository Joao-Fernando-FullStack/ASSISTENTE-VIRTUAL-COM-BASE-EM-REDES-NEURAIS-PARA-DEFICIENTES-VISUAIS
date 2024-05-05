import pyttsx3
speech_text = pyttsx3.init()


def voice_speech(text):
    speech_text.setProperty('rate', 220)  # velocidade da fala
    voices = speech_text.getProperty('voices')
    speech_text.setProperty('voices', voices[1].id)  # alterar voz
    speech_text.say(text)
    speech_text.runAndWait()


try:
    from urllib.error import URLError
    from AVA.ControladorDispositivo import controladorDispositivoArduino
    from AVA.Functions import latestnews, obter_clima_atual, _hora, _data, greeting_message, enviar_mensagem_whatsapp, \
    speech_recognition, _pesquisar, _lembrete, mostrar_lista_tarefas, adicionar_tarefa, \
    apagar_lista_tarefas, hotword, tocarMusica, encerrar, pesquisarWikipedia, piadas,tradutor
except Exception as ex:
    voice_speech('Desculpe, Para ativar o Assistente Virtual Athena tem que conectar a Internet... Obrigado!')


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
        tocarMusica()
    elif "notícias" in comando:
        latestnews()
    elif "wikipédia" in comando:
        pesquisarWikipedia()
    elif "piadas" in comando:
        piadas()
    elif "tradutor" in comando:
        tradutor()

    elif "whatsapp" in comando:
        try:
            voice_speech('Diz o número do telefone que desja enviar mensagem!')
            numero = "+244" + speech_recognition().lower()
            voice_speech('Diga a mensagem que deseja enviar')
            mensagem = speech_recognition().lower()
            enviar_mensagem_whatsapp(numero, mensagem, atraso_segundos=60)
        except Exception as e:
            voice_speech('Desculpe, Erro! ao tentar enviar mensagem, verifique o número!')


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


