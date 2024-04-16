import speech_recognition as sr
from dados_de_treinamento import commands_responses  # Importar o dicionário de comandos e respostas

# Função para processar a entrada do usuário e identificar o comando
def process_input(input_text):
    # Convertendo para minúsculas para facilitar a comparação
    input_text = input_text.lower()
    for command in commands_responses:
        if command in input_text:
            return command
    return None

# Função principal para capturar a entrada de voz e interagir com o assistente
def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Diga algo:")
        audio = r.listen(source)

    try:
        print("Reconhecendo...")
        user_input = r.recognize_google(audio, language='pt-BR')
        print("Você disse:", user_input)

        command = process_input(user_input)
        if command:
            response = commands_responses[command]
            print("Assistente:", response)
        else:
            print("Comando não reconhecido.")

    except sr.UnknownValueError:
        print("Desculpe, não entendi o áudio.")
    except sr.RequestError as e:
        print("Não foi possível fazer a requisição; {0}".format(e))

if __name__ == "__main__":
    main()

