# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:17:40 2018
"""
import pygame
from random import randrange

#Baseado no canla do Youtube KidsCanCode
#===========================   Classes   ===========================#
class Nave(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.radius = 50 
        self.rect.y = pos_y
        self.rect.x = pos_x
        
    def shoot(self):
        tiro = Tiros('Assets/tiro1.png', self.rect.x + 35, self.rect.top, 10)
        tudo.add(tiro)
        bullets_group.add(tiro)
        
class Tiros(pygame.sprite.Sprite):
    def __init__(self, arquivo_imagem, pos_x, pos_y, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.rect.bottom = pos_y
        self.rect.x = pos_x
        self.vy = -vy
        
    def update(self):
        self.rect.y += self.vy
        if self.rect.bottom < 0:
            self.kill()
            
class Inimigos(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem, pos_x, pos_y, vy, vx):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.radius = 56
        self.rect.y = pos_y
        self.rect.x = pos_x
        self.vy = vy
        self.vx = vx
        
    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if self.rect.top > 700 or self.rect.left < 0 or self.rect.right > 1200:
            self.rect.y = randrange(-100, -40)
            self.rect.x = randrange(0, 1200)
            self.vy = randrange(1, 8)
            self.vx = randrange(-3,3)
            

#===========================   Iniciar   ===========================#
pygame.init()

WIDTH = 1200
HEIGHT = 700

enemy_group = pygame.sprite.Group()
nave_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
tudo = pygame.sprite.Group()

tela = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('2D Shooter')

fundo = pygame.image.load("Assets/SpaceBackground.png").convert()

nave = Nave('Assets/MilleniumFalcon.png', WIDTH/2, HEIGHT - 100)
nave_group.add(nave)

#outra_nave = Nave('Assets/X-Wing.png', 600, 595)
#nave_group.add(outra_nave)

for i in range(3):
    meteor = Inimigos('Assets/meteor.gif', randrange(0, 1200),\
                randrange(-100, -40), randrange(1, 8), randrange(-3,3))
    tudo.add(meteor)
    enemy_group.add(meteor)
    
tudo.add(enemy_group)
tudo.add(nave_group)
#===========================   ''   ===========================#
relogio =  pygame.time.Clock()
score = 0
FPS = 120
y = 0


Game = True
paused = False
while Game:
    tempo = relogio.tick(FPS)

    pressed_keys = pygame.key.get_pressed()
    
    if pressed_keys[pygame.K_ESCAPE]:
        Game = False
    
#MOVER NAVE 1
    """ Movimento Vertical e Horizontal """
    if pressed_keys[pygame.K_LEFT] and nave.rect.x >= 5:
        nave.rect.x -= 5
    if pressed_keys[pygame.K_UP] and nave.rect.y >= 5:
        nave.rect.y -= 5
    if pressed_keys[pygame.K_RIGHT] and nave.rect.x <= (WIDTH -\
                   5 - nave.rect.width):
        nave.rect.x += 5
    if pressed_keys[pygame.K_DOWN] and nave.rect.y <= (HEIGHT -\
                   5 - nave.rect.height):
        nave.rect.y += 5
    """ Movimento Diagonal """
    # xˆ2 + xˆ2 = 25 => 2xˆ2 = 25 => xˆ2 = 25/2 => x = 12.5ˆ(1/2) 
    if pressed_keys[pygame.K_LEFT] and pressed_keys[pygame.K_UP] and \
    nave.rect.x >= 5 and nave.rect.y >= 5:
        nave.rect.x -= 12.5 ** (1/2)
        nave.rect.y -= 12.5 ** (1/2)
    if pressed_keys[pygame.K_LEFT] and pressed_keys[pygame.K_DOWN] and \
    nave.rect.x >= 5 and nave.rect.y <= (HEIGHT - 5 - nave.rect.height):
        nave.rect.x -= 12.5 ** (1/2)
        nave.rect.y += 12.5 ** (1/2)
    if pressed_keys[pygame.K_RIGHT] and pressed_keys[pygame.K_DOWN] and \
    nave.rect.x <= (WIDTH - 5 - nave.rect.width) and nave.rect.y <=\
    (HEIGHT - 5 - nave.rect.height):
        nave.rect.x += 12.5 ** (1/2)
        nave.rect.y += 12.5 ** (1/2)
    if pressed_keys[pygame.K_RIGHT] and pressed_keys[pygame.K_UP] and \
    nave.rect.x <= (WIDTH - 5 - nave.rect.width) and nave.rect.y >= 5:
        nave.rect.x += 12.5 ** (1/2)
        nave.rect.y -= 12.5 ** (1/2)
    
#MOVER NAVE 2
#    if pressed_keys[K_a] and outra_nave.rect.x >= 5:
#        outra_nave.rect.x -= 5
#    if pressed_keys[K_d] and outra_nave.rect.x <= (1195 - outra_nave.rect.width):
#        outra_nave.rect.x += 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:            
            Game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                nave.shoot()
            
#MOVIMENTO DA TELA#
    rel_y = y % fundo.get_rect().height
    tela.blit(fundo, (0, rel_y - fundo.get_rect().height))
    if rel_y < HEIGHT:
        tela.blit(fundo, (0, rel_y))
    y += 3
    
    tudo.update()
    
    hits = pygame.sprite.spritecollide(nave, enemy_group, False)
    if hits:
        Game = False
    
    tiros = pygame.sprite.groupcollide(enemy_group, bullets_group, True, True)
    for tiro in tiros:
        meteor = Inimigos('Assets/meteor.gif', randrange(0, 1200),\
                randrange(-100, -40), randrange(1, 8), randrange(-3,3))
        tudo.add(meteor)
        enemy_group.add(meteor)
        
        score += 1          #colocar no próprio jogo depois
        print(score)        

    tudo.draw(tela)
    pygame.display.flip()
    
pygame.display.quit()