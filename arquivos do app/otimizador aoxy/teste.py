import pygame
import sys

pygame.init()

largura = 800
altura = 600
tela = pygame.display.set_mode((largura,altura))

pygame.display.set_caption("minha primeira janela!")

cor_fundo = (50, 150, 200)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    tela.fill(cor_fundo)

    pygame.display.update()
