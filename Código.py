# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:17:40 2018
"""
import pygame
from random import randrange
import random
from os import path
#Baseado no canal do Youtube KidsCanCode 
#https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg

#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> 
#licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
#===========================   Classes   ===========================#
    
class Nave(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.radius = 48
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 5
        self.vx = 0
        
    def update(self):
        self.vx = 0
        self.vy = 0
        keystate = pygame.key.get_pressed()
        """ MOVIMENTO HORIZONTAL E VERTICAL """
        if keystate[pygame.K_LEFT] and not keystate[pygame.K_UP] and not\
        keystate[pygame.K_DOWN] and not keystate[pygame.K_RIGHT]:
            self.vx = -5
        if keystate[pygame.K_RIGHT] and not keystate[pygame.K_UP] and not \
        keystate[pygame.K_DOWN] and not keystate[pygame.K_LEFT]:
            self.vx = 5
        if keystate[pygame.K_UP] and not keystate[pygame.K_RIGHT] and not \
        keystate[pygame.K_DOWN] and not keystate[pygame.K_LEFT]:
            self.vy = -5
        if keystate[pygame.K_DOWN] and not keystate[pygame.K_UP] and not \
        keystate[pygame.K_RIGHT] and not keystate[pygame.K_LEFT]:
            self.vy = 5
        """ MOVIMENTO DIAGONAL """ 
        # xˆ2 + xˆ2 = 25 => 2xˆ2 = 25 => xˆ2 = 25/2 => x = 12.5ˆ(1/2)
        if keystate[pygame.K_LEFT] and keystate[pygame.K_UP]:
            self.vx = -(12.5 ** (1/2))
            self.vy = -(12.5 ** (1/2))
        if keystate[pygame.K_LEFT] and keystate[pygame.K_DOWN]:
            self.vx = -(12.5 ** (1/2))
            self.vy = (12.5 ** (1/2))
        if keystate[pygame.K_RIGHT] and keystate[pygame.K_DOWN]:
            self.vx = (12.5 ** (1/2))
            self.vy = (12.5 ** (1/2))
        if keystate[pygame.K_RIGHT] and keystate[pygame.K_UP]:
            self.vx = (12.5 ** (1/2))
            self.vy = -(12.5 ** (1/2))
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right > WIDTH - 5:
            self.rect.right = WIDTH - 5
        if self.rect.left < 5:
            self.rect.left = 5
        if self.rect.bottom > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5
        if self.rect.top < 5:
            self.rect.top = 5
        
    def shoot(self, tudo, bullets_group):
        tiro = Tiros('Assets/tiro1.png', self.rect.centerx, self.rect.top)
        tudo.add(tiro)
        bullets_group.add(tiro)
        shoot_sound.play()
        
class Tiros(pygame.sprite.Sprite):
    def __init__(self, arquivo_imagem, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.rect.bottom = pos_y
        self.rect.centerx = pos_x
        self.vy = -10
        
    def update(self):
        self.rect.y += self.vy
        if self.rect.bottom < 0:
            self.kill()
            
class Inimigos(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.radius = 43
        self.rect.x = randrange(0, 1200)
        self.rect.y = randrange(-150, -100)
        self.vy =  randrange(1, 8)
        self.vx =  randrange(-3, 3)
        
    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if self.rect.top > HEIGHT or self.rect.right < 0 or \
        self.rect.left > WIDTH:
            self.rect.y = randrange(-100, -40)
            self.rect.x = randrange(0, 1200)
            self.vy = randrange(1, 8)
            self.vx = randrange(-3,3)
            
#===========================   Cores     ===========================#
GREEN = (0, 150, 0)
LIGHTGREEN = (0, 255, 0)
RED = (150, 0, 0)
LIGHTRED = (255, 0, 0)
BLUE = (0, 0, 150)
LIGHTBLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#===========================   Funções   ===========================#   
def mensagem(mensagem, x, y, tamanho, COR):
   
    def textos(mensagem, fonte):
        textSurface = fonte.render(mensagem, True, COR)
        return textSurface, textSurface.get_rect()

    texto = pygame.font.SysFont('agencyfb', tamanho)
    TextSurf, TextRect = textos(mensagem, texto)
    TextRect.center = (x, y)
    tela.blit(TextSurf, TextRect)

def sair():
    pygame.quit()
    quit()

def botao(msg, x, y, w, h, cor, cor_mouse):
    mouse = pygame.mouse.get_pos()
        
    if x + w > mouse[0] > x and\
    y + h > mouse[1] > y:
        pygame.draw.rect(tela, cor_mouse, (x, y, w, h))
            
    else:
        pygame.draw.rect(tela, cor, (x, y, w, h))
    
    mensagem(msg, x + (w/2),  y + (h/2), 40, WHITE)
    
musics = ['tgfcoder-FrozenJam-SeamlessLoop.ogg', 'SW.ogg', 'DV.ogg']

def Musicas(mus):
    musica = musics[mus]
    pygame.mixer.music.load(path.join(snd_dir,
                                  musica))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops = -1)
    
def main():
    loop = True
    intro = True
    instruction = False
    Game = False
    while loop:
        x = 0
        mn = pygame.image.load("Assets/SpaceBackground.png").convert()
        Musicas(1)
        while intro:
            pressed_keys = pygame.key.get_pressed()
            
            if pressed_keys[pygame.K_ESCAPE]:
                Game = False
                intro = False
                instruction = False
                loop = False
            if pressed_keys[pygame.K_RETURN]:
                Game = True
                intro = False
                instruction = False
            if pressed_keys[pygame.K_i]:
                Game = False
                intro = False
                instruction = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            rel_x = x % mn.get_rect().width
            tela.blit(mn, (rel_x - mn.get_rect().width, 0))
            if rel_x < WIDTH:
                tela.blit(mn, (rel_x, 0))
            x += 2
            
            mensagem('GUARDIANS', WIDTH/2, HEIGHT/2 - 250, 130, YELLOW)
            mensagem('OF THE', WIDTH/2, HEIGHT/2 - 175, 30, YELLOW)
            mensagem('UNIVERSE', WIDTH/2, HEIGHT/2 - 100, 130, YELLOW)
            
            mensagem('Press Enter to Play', WIDTH/2, HEIGHT/2 + 20, 50, LIGHTGREEN)
            mensagem('Press I for Instructions', WIDTH/2, HEIGHT/2 + 120, 50,
                     LIGHTBLUE)
            mensagem('Press ESC to Quit', WIDTH/2, HEIGHT/2 + 220, 50, LIGHTRED)
            
            
            
            pygame.display.update()
            relogio.tick(FPS)
    
        x = 0
        inst = pygame.image.load("Assets/SpaceBackground.png").convert()
        while instruction:
            
            pressed_keys = pygame.key.get_pressed()
            
            if pressed_keys[pygame.K_RETURN]:
                Game = True
                intro = False
                instruction = False
            if pressed_keys[pygame.K_q]:
                Game = False
                intro = True
                instruction = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            tela.fill(BLACK)
            rel_x = x % inst.get_rect().width
            tela.blit(inst, (rel_x - inst.get_rect().width, 0))
            if rel_x < WIDTH:
                tela.blit(inst, (rel_x, 0))
            x -= 2
            
            mensagem('INSTRUCTIONS', WIDTH/2, HEIGHT/2 - 200, 130, WHITE)
            mensagem('Shoot: SPACE', WIDTH/2, HEIGHT/2 - 100, 50, WHITE)
            mensagem('Move: Arrow Keys', WIDTH/2, HEIGHT/2 - 50, 50, WHITE)
            mensagem('Pause: P',  WIDTH/2, HEIGHT/2, 50, WHITE)
            
            mensagem('Press Q to go back to the Menu', WIDTH/2,
                     HEIGHT/2 + 200, 50, LIGHTRED)
            mensagem('Press Enter to Play', WIDTH/2, HEIGHT/2 + 100, 50, 
                  LIGHTGREEN)
            
            pygame.display.update()
            relogio.tick(FPS)
        
        enemy_group = pygame.sprite.Group()
        nave_group = pygame.sprite.Group()
        bullets_group = pygame.sprite.Group()
        tudo = pygame.sprite.Group()
            
        fundo = pygame.image.load("Assets/SpaceBackground.png").convert()
        
        nave = Nave('Assets/MilleniumFalcon.png')
        nave_group.add(nave)
    
        for i in range(8):
            meteor = Inimigos('Assets/meteor.gif')
            tudo.add(meteor)
            enemy_group.add(meteor)
            
        tudo.add(enemy_group)
        tudo.add(nave_group)
        score = 0
        y = 0
        Musicas(0)
        fundo = pygame.image.load("Assets/SpaceBackground.png").convert()
        while Game:
            relogio.tick(FPS)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:            
                    Game = False
                    loop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        nave.shoot(tudo, bullets_group)
                    elif event.key == pygame.K_p:
                        pause = True
                        while pause:
                            
                            pressed_keys = pygame.key.get_pressed()
                        
                            if pressed_keys[pygame.K_q]:
                                Game = False
                                intro = True
                                instruction = False
                                pause = False
                            
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_p:
                                        pause = False
                                    
                            mensagem('PAUSED', WIDTH/2, HEIGHT/2 - 100, 130,
                                     WHITE)
                            mensagem('Press any key to continue', WIDTH/2,
                                     HEIGHT/2, 50, WHITE)
                            
                            mensagem('Press Q to go back to the Menu',
                                     WIDTH/2, HEIGHT/2 + 100, 50, LIGHTRED)
                            
                            pygame.display.update()
                            relogio.tick(FPS)
                    
            """MOVIMENTO DA TELA"""
            rel_y = y % fundo.get_rect().height
            tela.blit(fundo, (0, rel_y - fundo.get_rect().height))
            if rel_y < HEIGHT:
                tela.blit(fundo, (0, rel_y))
            y += 10
            
            tudo.update()
            
            hits = pygame.sprite.spritecollide\
            (nave, enemy_group, False, pygame.sprite.collide_circle)
            if hits:
                crash_sound.play()
                Game = False
                Musicas(2)
                over = True
                x = 0
                go = pygame.image.load("Assets/SpaceBackground.png").convert()
                while over:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    
                    pressed_keys = pygame.key.get_pressed()
                    
                    if pressed_keys[pygame.K_r]:
                        over = False
                        Game = True
                        loop = True
                        intro = False
                        instruction = False
                        
                        enemy_group = pygame.sprite.Group()
                        nave_group = pygame.sprite.Group()
                        bullets_group = pygame.sprite.Group()
                        tudo = pygame.sprite.Group()
                            
                        fundo = pygame.image.load("Assets/SpaceBackground.png").convert()
                        
                        nave = Nave('Assets/MilleniumFalcon.png')
                        nave_group.add(nave)
                        
                        for i in range(8):
                            meteor = Inimigos('Assets/meteor.gif')
                            tudo.add(meteor)
                            enemy_group.add(meteor)
                            
                        tudo.add(enemy_group)
                        tudo.add(nave_group)
                        Musicas(0)
                        
                    if pressed_keys[pygame.K_q]:
                        over = False
                        intro = True
                        instruction = False
                        Game = False
                        loop = True
                        
                    tela.fill(BLACK)
                    rel_x = x % go.get_rect().width
                    tela.blit(go, (rel_x - go.get_rect().width, 0))
                    if rel_x < WIDTH:
                        tela.blit(go, (rel_x, 0))
                    x += 2
                        
                    mensagem('GAME OVER', WIDTH/2, HEIGHT/2 - 100, 130, WHITE)
                    mensagem('Press R to restart', WIDTH/2, HEIGHT/2 + 10, 50,
                             LIGHTGREEN)
                    mensagem('Press Q to go back to the Menu', WIDTH/2,
                             HEIGHT/2 + 100, 50, LIGHTRED)
                    
                    pygame.display.update()
                    relogio.tick(FPS)
            
            tiros = pygame.sprite.groupcollide(enemy_group, bullets_group, True,
                                               True)
            for tiro in tiros:
                random.choice(exp_sounds).play()
                meteor = Inimigos('Assets/meteor.gif')
                tudo.add(meteor)
                enemy_group.add(meteor)        
                score += 100  
            
            if Game:
                tudo.draw(tela)
                mensagem('{0}' .format(score), WIDTH/2, 20, 30, YELLOW)
                pygame.display.flip()
        
#===========================   'Iniciar'   ===========================#
pygame.init()
pygame.font.init()

WIDTH = 1200
HEIGHT = 700

tela = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('2D Shooter')

#===========================       'Som'         ===========================#
snd_dir = path.join(path.dirname (__file__), 'snd')
pygame.mixer.init()

#som do tiro
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser.wav'))

#sons da explosão
exp_sounds = []
for snd in ['Explosion1.wav', 'Explosion2.wav']:
    exp_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    
#som da morte
crash_sound = pygame.mixer.Sound(path.join(snd_dir, 'Crash.wav'))

#som do background

#===========================   'Funcionamento'   ===========================#
relogio =  pygame.time.Clock()
FPS = 120

main()