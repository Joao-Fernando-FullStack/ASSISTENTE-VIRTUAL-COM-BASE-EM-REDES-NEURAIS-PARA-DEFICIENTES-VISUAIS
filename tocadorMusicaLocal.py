import os
import pygame

def tocar_musica(caminho_musica, titulo):
    musicas = os.listdir(caminho_musica)  # Obtém a lista de arquivos no diretório especificado

    # Procura pela música com o título mencionado
    for musica in musicas:
        if titulo.lower() in musica.lower():
            caminho_completo = os.path.join(caminho_musica, musica)
            pygame.mixer.init()

            try:
                pygame.mixer.music.load(caminho_completo)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except pygame.error:
                print("Erro ao reproduzir a música.")

# Diretório onde suas músicas estão armazenadas
caminho_das_musicas = "C:/Users/PC/Music"

# Captura do título da música digitado pelo usuário
titulo_musica = input("Digite o título da música: ")

# Toca a música com o título fornecido e o caminho específico
tocar_musica(caminho_das_musicas, titulo_musica)


