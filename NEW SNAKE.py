import pygame
import os
from RANKING import *
from random import randint

pygame.display.set_caption("SNAKE")

TELA_LARGURA = 800 #x
TELA_ALTURA = 600 #y


RANKING = "RANKING.txt"
if not arquivoExiste(RANKING):
    criararquivo(RANKING)

IMAGEM_COBRA = pygame.image.load(os.path.join("imagens", "COBRA.PNG"))  # por enquanto somente a cabeça
IMAGEM_CENARIO = pygame.image.load(os.path.join("imagens", "CENARIO.JPG"))  # procurar imagens nova ou imagens variadas
IMAGEM_COMIDA = pygame.image.load(os.path.join("imagens", "COMIDA.PNG"))  # procurar comida especial
IMAGEM_MENU = pygame.image.load(os.path.join("imagens", "MENU.JPG"))  # Melhor menu com varios opções
IMAGEM_MENU = pygame.transform.scale(IMAGEM_MENU, (TELA_LARGURA, TELA_ALTURA))
# criar um menu de histórico de pontos

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 30)

# CORES RGB
BRANCA = (255, 255, 255)
AZUL = (0, 0, 255)

# paramentros do jogo
QUADRADO = 20
ATUALIZACAO = 15
PONTUACAO = 0
NOME = ""

###################################################### MENU #########################################

tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
fonte = pygame.font.Font(None, 40)
cor_texto = (255, 255, 255)
cor_confirmar = (0, 255, 0)
cor_texto_confirmar = (0, 0, 0)

def exibir_menu():
    global NOME

    inserindo_nome = True
    while inserindo_nome:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                inserindo_nome = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and NOME != "":  # Quando o jogador pressiona Enter e há um nome inserido
                    inserindo_nome = False
                elif evento.key == pygame.K_BACKSPACE:  # Remove o último caractere
                    NOME = NOME[:-1]
                else:
                    NOME += evento.unicode  # Adiciona o caractere digitado à variável NOME

        # Desenha o fundo do menu
        tela.blit(IMAGEM_MENU, (0, 0))

        # Renderiza o nome na tela
        texto_nome = fonte.render(f"Nome: {NOME}", True, cor_texto)
        tela.blit(texto_nome, (250, 300))

        # Desenha o botão de confirmar
        largura_botao, altura_botao = 200, 60
        x_botao = (TELA_LARGURA - largura_botao) // 2
        y_botao = 400
        pygame.draw.rect(tela, cor_confirmar, (x_botao, y_botao, largura_botao, altura_botao))
        
        # Renderiza o texto "Confirmar" no botão
        texto_confirmar = fonte.render("Confirmar", True, cor_texto_confirmar)
        tela.blit(texto_confirmar, (x_botao + 20, y_botao + 10))

        # Detectar clique do mouse no botão de confirmar
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Verifica se o botão esquerdo foi pressionado
            if x_botao < mouse_pos[0] < x_botao + largura_botao and y_botao < mouse_pos[1] < y_botao + altura_botao:
                if NOME != "":  # O nome precisa estar preenchido para confirmar
                    inserindo_nome = False

        # Atualiza a tela
        pygame.display.flip()

# Exibir o menu
exibir_menu()
class Cobra:

    def __init__(self, largura, altura):
        self.tamanho = 1
        self.pixels = []
        self.velocidadeX = 0
        self.velocidadeY = 0
        self.x = round((largura / 2) / 20) * 20
        self.y = round((altura / 2) / 20) * 20

    def desenhar(self, tela, tamanho):
        self.pixels.append([self.x, self.y])
        if len(self.pixels) > self.tamanho:
            del (self.pixels[0])

        #melhorar estrutura
        # cabeca = len(self.pixels) - 1
        #tela.blit(IMAGEM_COBRA, (self.pixels[cabeca][0], self.pixels[cabeca][1]))
        for pixel in self.pixels:
            pygame.draw.rect(tela, (150, 90, 79), (pixel[0], pixel[1], 20, 20))


        self.x += self.velocidadeX
        self.y += self.velocidadeY
        self.tamanho = tamanho + 1

    def mover(self, tecla):

        if self.velocidadeY == 0:
            if tecla == pygame.K_DOWN or tecla == pygame.K_s:
                self.velocidadeX = 0
                self.velocidadeY = QUADRADO
            elif tecla == pygame.K_UP or tecla == pygame.K_w:
                self.velocidadeX = 0
                self.velocidadeY = -QUADRADO
        if self.velocidadeX == 0:
            if tecla == pygame.K_RIGHT or tecla == pygame.K_d:
                self.velocidadeX = QUADRADO
                self.velocidadeY = 0
            elif tecla == pygame.K_LEFT or tecla == pygame.K_a:
                self.velocidadeX = -QUADRADO
                self.velocidadeY = 0

    def atravessar(self):
        if self.x < 0:
            self.x = TELA_LARGURA - QUADRADO

        elif self.x == TELA_LARGURA:
            self.x = 0

        elif self.y < 0:
            self.y = TELA_ALTURA - QUADRADO

        elif self.y == TELA_ALTURA:
            self.y = 0


class Comida:
    def __init__(self):
        self.pontos = 1
        self.x = round(randint(0, TELA_LARGURA - QUADRADO) / 20) * 20
        self.y = round(randint(0, TELA_ALTURA - QUADRADO) / 20) * 20
        self.especial = False
        self.contador = 0

    def desenhar(self, tela, x, y):
        global PONTUACAO

        if x == self.x and y == self.y:
            self.contador += 1
            self.x = round(randint(0, TELA_LARGURA - QUADRADO) / 20) * 20
            self.y = round(randint(0, TELA_ALTURA - QUADRADO) / 20) * 20

            if self.contador % 10 == 0:
                PONTUACAO += 100
            else:
                PONTUACAO += 10

        tela.blit(IMAGEM_COMIDA, (self.x, self.y))


def main():
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    relogio = pygame.time.Clock()  # controle do tempo

    cobra = Cobra(TELA_LARGURA, TELA_ALTURA)
    comida = Comida()

    rodando = True
    while rodando:
        # desenha fundo da tela
        tela.blit(IMAGEM_CENARIO, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                cobra.mover(evento.key)

        # desenha pontuação
        texto = FONTE_PONTOS.render(f'Pontuação: {PONTUACAO}', True, AZUL)
        tela.blit(texto, [0, 0])

        # atravessando a tela
        cobra.atravessar()

        # desenhar comida
        comida.desenhar(tela, cobra.x, cobra.y)

        # desenhar cobra
        cobra.desenhar(tela, comida.contador)


        for pixel in cobra.pixels[:-1]:
            if pixel == [cobra.x, cobra.y]:
                rodando = False

        pygame.display.update()
        relogio.tick(ATUALIZACAO)

exibir_menu()
main()
cadastrar(RANKING, NOME, PONTUACAO)
lerarquivos(RANKING)