# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:17:40 2018
"""
import pygame
from pygame.locals import *
from random import randrange
#===========================   Classes   ===========================#
class Nave(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.rect.y = pos_y
        self.rect.x = pos_x

class Inimigos(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem, pos_x, pos_y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.rect.y = pos_y
        self.rect.x = pos_x
        self.vx = vx
        self.vy = vy
        
    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
#===========================   Iniciar   ===========================#
pygame.init()

tela = pygame.display.set_mode((1200, 700), 0, 32)
pygame.display.set_caption('2D Shooter')

fundo = pygame.image.load("Assets/SpaceBackground.png").convert()
y = 0

nave = Nave('Assets/MilleniumFalcon.png', 600, 595)
nave_group = pygame.sprite.Group()
nave_group.add(nave)

#outra_nave = Nave('', 400, 800)
#nave.group.add(outra_nave)

#inimigo1 = Inimigos('Assets/Inimigo1.png', 0, 0,\
#                    randrange(-10,10), randrange(-10, 10))
#===========================   ''   ===========================#
relogio =  pygame.time.Clock()
score = 0

Game = True
while Game:
    tempo = relogio.tick(120)
    
    pressed_keys = pygame.key.get_pressed()
#MOVER AS NAVES
    if pressed_keys[K_LEFT] and nave.rect.x >= 5:
        nave.rect.x -= 5
    
    if pressed_keys[K_RIGHT] and nave.rect.x <= (1195 - nave.rect.width):
        nave.rect.x += 5
    
#   if pressed_keys[K_LEFT]:
#       outra_raquete.rect.x -= 5
#   elif pressed_keys[K_RIGHT]:
#       outra_raquete.rect.x += 5
        
    for event in pygame.event.get():
        if event.type == QUIT:            
            Game = False

    rel_y = y % fundo.get_rect().height
    tela.blit(fundo, (0, rel_y - fundo.get_rect().height))
    if rel_y < 700:
        tela.blit(fundo, (0, rel_y))
    y += 2
    
    nave_group.draw(tela)
#   inimigos_group.draw(tela)
    
    pygame.display.update()
    
pygame.display.quit()