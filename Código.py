# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:17:40 2018
"""

import pygame

#===========================   Classes   ===========================#
class Nave(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.rect.y = pos_y
        self.rect.x = pos_x
        
#===========================   Iniciar   ===========================#
pygame.init()

tela = pygame.display.set_mode((1200, 700), 0, 32)
pygame.display.set_caption('2D Shooter')

fundo = pygame.image.load("").convert()

nave = Nave('Assets/Millenium Falcon.png', 600, 800)
nave_group = pygame.sprite.Group()
nave_group.add(nave)

#outra_nave = Nave('', 400, 800)
#nave.group.add(outra_nave)
#===========================   ''   ===========================#
relogio =  pygame.time.Clock()
score = 0

Game = True
while Game:
    tempo = relogio.tick(120)
    
    pressed_keys = pygame.key.get_pressed()
#MOVER AS NAVES
    if pressed_keys[pygame.K_a]:
        nave.rect.x -= 5
    elif pressed_keys[pygame.K_d]:
        nave.rect.x += 5
#   if pressed_keys[pygame.K_LEFT]:
#       outra_raquete.rect.x -= 5
#   elif pressed_keys[pygame.K_RIGHT]:
#       outra_raquete.rect.x += 5
        
    for event in pygame.event.get():
        # Verifica se o evento atual é QUIT (janela fechou).
        if event.type == pygame.QUIT or event.type == pygame.ESCAPE:            
            # Neste caso, marca o flag rodando como False, 
            # para sair do loop de jogo.
            rodando = False

#if nave.rect.x < 0 or nave.rect.x >= (800 - nave.rect.width):
#        if bola.rect.x < 0:
#            
#       else:

    tela.blit(fundo, (0, 0))
    nave_group.draw(tela)
#   inimigos_group.draw(tela)
    
    pygame.display.update()
    
pygame.display.quit()
            