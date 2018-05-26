# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:17:40 2018

Baseado no canal do Youtube KidsCanCode 
https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg

Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> 
licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

Cosmic Storm by A Himitsu https://soundcloud.com/a-himitsu
Creative Commons — Attribution 3.0 Unported— CC BY 3.0 
http://creativecommons.org/licenses/b...
Music promoted by Audio Library https://youtu.be/U4wXUdhNxZk

Battle (Boss) by BoxCat Games http://freemusicarchive.org/music/Box...
Creative Commons — Attribution 3.0 Unported— CC BY 3.0 
http://creativecommons.org/licenses/b...
Music promoted by Audio Library https://youtu.be/F-vl7Djb96o
"""
import pygame
from random import randrange
import random
from os import path
import os
import time

#==============================     Classes     ==============================#
class Nave(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem, speed, shield):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width / 2) - 2
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 5
        self.vx = 0
        self.vy = 0
        self.speed = speed
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.shield = shield
        self.lives = 3
        self.nukes = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
        
    def update(self):
        self.vx = 0
        self.vy = 0
        keystate = pygame.key.get_pressed()
        if self.power>=2 and pygame.time.get_ticks() - self.power_time > 5000:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        """ MOVIMENTO HORIZONTAL E VERTICAL """
        if keystate[pygame.K_LEFT] and not keystate[pygame.K_UP] and not\
        keystate[pygame.K_DOWN] and not keystate[pygame.K_RIGHT]:
            self.vx = -self.speed
        if keystate[pygame.K_RIGHT] and not keystate[pygame.K_UP] and not \
        keystate[pygame.K_DOWN] and not keystate[pygame.K_LEFT]:
            self.vx = self.speed
        if keystate[pygame.K_UP] and not keystate[pygame.K_RIGHT] and not \
        keystate[pygame.K_DOWN] and not keystate[pygame.K_LEFT]:
            self.vy = -self.speed
        if keystate[pygame.K_DOWN] and not keystate[pygame.K_UP] and not \
        keystate[pygame.K_RIGHT] and not keystate[pygame.K_LEFT]:
            self.vy = self.speed
        """ MOVIMENTO DIAGONAL """ 
        # xˆ2 + xˆ2 = 25 => 2xˆ2 = 25 => xˆ2 = 25/2 => x = 12.5ˆ(1/2)
        if keystate[pygame.K_LEFT] and keystate[pygame.K_UP]:
            self.vx = -(((self.speed ** 2) / 2) ** (1/2))
            self.vy = -(((self.speed ** 2) / 2) ** (1/2))
        if keystate[pygame.K_LEFT] and keystate[pygame.K_DOWN]:
            self.vx = -(((self.speed ** 2) / 2) ** (1/2))
            self.vy = ((self.speed ** 2) / 2) ** (1/2)
        if keystate[pygame.K_RIGHT] and keystate[pygame.K_DOWN]:
            self.vx = ((self.speed ** 2) / 2) ** (1/2)
            self.vy = ((self.speed ** 2) / 2) ** (1/2)
        if keystate[pygame.K_RIGHT] and keystate[pygame.K_UP]:
            self.vx = ((self.speed ** 2) / 2) ** (1/2)
            self.vy = -(((self.speed ** 2) / 2) ** (1/2))
        '''Impedindo a saida da tela'''
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
        
        if self.lives > 1:
            if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
                self.hidden = False
            
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
    
    def nuke(self, enemy_group, tudo, boss, boss_alive, score, nave, stalkers,
             lista_meteoros, mobs, lista_atirador):
        for enemy in enemy_group:
            expl = Explosion(enemy.rect.center, 'lg')
            enemy.kill()
            tudo.add(expl)
        if boss_alive:
            boss_expl = Explosion(boss.rect.center, 'boss')
            boss.shield -= 200
            tudo.add(boss_expl)
            tudo.add()
        for i in range(4):
            if score < 1000:
                novo_meteoro(lista_meteoros, tudo, enemy_group)
            if score >= 1000 and score <= 2500:
                randchoice_enemy = [1, 2]
                resp = random.choice(randchoice_enemy)
                if resp == 1:
                    novo_meteoro(lista_meteoros, tudo, enemy_group)
                elif resp == 2:
                    novo_stalker(tudo, enemy_group, stalkers, nave, boss_alive)
            if score >= 2500 and score <= 5000:
                novo_atirador(tudo, enemy_group, mobs, lista_atirador)
            if score > 5000:
                randchoice_enemy = [1, 2, 3]
                resp = random.choice(randchoice_enemy)
                if resp == 1:
                    novo_meteoro(lista_meteoros, tudo, enemy_group)
                elif resp == 2:
                    novo_stalker(tudo, enemy_group, stalkers, nave, boss_alive)
                elif resp == 3:
                    novo_atirador(tudo, enemy_group, mobs, lista_atirador)
    
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
        
    def shoot(self, img_tiros, tudo, bullets_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
        if self.power == 1:
            tiro = Tiros(img_tiros, self.rect.centerx, self.rect.top)
            tudo.add(tiro)
            bullets_group.add(tiro)
            shoot_sound.play()
        if self.power == 2:
            tiro1 = Tiros(img_tiros, self.rect.left, self.rect.centery)
            tiro2 = Tiros(img_tiros, self.rect.right, self.rect.centery)
            tudo.add(tiro1)
            tudo.add(tiro2)
            bullets_group.add(tiro1)
            bullets_group.add(tiro2)
            shoot_sound.play()
        if self.power >= 3:
            tiro1 = Tiros(img_tiros, self.rect.left, self.rect.centery)
            tiro2 = Tiros(img_tiros, self.rect.right, self.rect.centery)
            tiro3 = Tiros(img_tiros, self.rect.centerx, self.rect.top)
            tudo.add(tiro1)
            tudo.add(tiro2)
            tudo.add(tiro3)
            bullets_group.add(tiro1)
            bullets_group.add(tiro2)
            bullets_group.add(tiro3)
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
            
class Meteoros(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(arquivo_imagem).convert()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.centerx = randrange(0, 1000)
        self.rect.centery = randrange(-150, -100)
        self.vy =  randrange(1, 8)
        self.vx =  randrange(-3, 3)
        self.rot = 0
        self.rot_speed = randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        self.rotacao()
        if self.rect.top > HEIGHT or self.rect.right < 0 or \
        self.rect.left > WIDTH:
            self.rect.y = randrange(-100, -40)
            self.rect.x = randrange(0, 1000)
            self.vy = randrange(1, 8)
            self.vx = randrange(-3,3)
            
    def rotacao(self):
        tempo = pygame.time.get_ticks()
        if tempo - self.last_update > 10:
            self.last_update = tempo
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                
class Nuke(pygame.sprite.Sprite):
    
    def __init__(self, center):
           self.image = 'Assets/Nuke.png'
           self.rect = self.image.get_rect()
           self.rect.center = center
           self.speedy = 2
           
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Pow(pygame.sprite.Sprite):
    
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['gun', 'shield'])
        self.image = powerups_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Stalker(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem, alvo):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(arquivo_imagem).convert()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.centery = randrange(-150, -100)
        self.rect.centerx = randrange(0, 1000)
        self.vy = 3
        self.alvo = alvo
        self.rot = 0
        self.rot_speed = randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
    def update(self):
        if self.rect.centerx > self.alvo.rect.centerx:
            self.vx = -2.5
        elif self.rect.centerx < self.alvo.rect.centerx:
            self.vx = 2.5
        else:
            self.vx = 0
        self.rect.centerx += self.vx
        self.rect.centery += self.vy
        self.rotacao()
        if self.rect.top > HEIGHT or self.rect.right < 0 or \
        self.rect.left > WIDTH:
            self.rect.y = randrange(-100, -40)
            self.rect.x = randrange(0, 1000)
    
    def rotacao(self):
        tempo = pygame.time.get_ticks()
        if tempo - self.last_update > 10:
            self.last_update = tempo
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Atirador(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.radius = 56
        self.rect.centery = randrange(-150, -100)
        self.rect.centerx = randrange(0, 1000)
        self.vy = 4
        self.vx = randrange(-5,5,2)
            
    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if self.rect.right > WIDTH - 5:
            self.rect.right = WIDTH - 5
            self.vx = -self.vx
        if self.rect.left < 5:
            self.rect.left = 5
            self.vx = -self.vx
        if self.rect.bottom > 150:
            self.rect.bottom = 150
                
    def enemy_shoot(self, tudo, enemy_bullets):
        tiro = Enemybullets('Assets/tiro_inimigo.png',
                            self.rect.centerx,
                            self.rect.bottom, 0)
        tiro1 = Enemybullets('Assets/tiro_inimigo_direita.png',
                             self.rect.centerx,
                             self.rect.bottom, 3)
        tiro2 = Enemybullets('Assets/tiro_inimigo_esquerda.png',
                             self.rect.centerx,
                             self.rect.bottom, -3)
        tudo.add(tiro)
        tudo.add(tiro1)
        tudo.add(tiro2)
        enemy_bullets.add(tiro)
        enemy_bullets.add(tiro1)
        enemy_bullets.add(tiro2)
        enemy_shoot_sound.play()

class Enemybullets(pygame.sprite.Sprite):
    def __init__(self, arquivo_imagem, pos_x, pos_y, vx):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.rect.centery = pos_y
        self.rect.centerx = pos_x
        self.vy = 3
        self.vx = vx
        
    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if self.rect.top > 600:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self, arquivo_imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.radius = 100
        self.rect.centery = randrange(-150, -100)
        self.rect.centerx = WIDTH / 2
        self.vy = 1
        self.shield = 750
        self.lives = 1
            
    def update(self):
        self.rect.y += self.vy
        if self.rect.bottom > 150:
            self.rect.bottom = 150
        
    def enemy_shoot(self, tudo, enemy_bullets):
        vxt1 = randrange(1, 4)
        vxt2 = randrange(vxt1 + 1, vxt1 + 4)
        vxt3 = randrange(vxt2 + 1, vxt2 + 4)
        
        tiro = Enemybullets('Assets/BossAttack.png',
                            self.rect.centerx,
                            self.rect.bottom, 0)
        tiro1 = Enemybullets('Assets/BossAttack.png',
                             self.rect.centerx,
                             self.rect.bottom, vxt1)
        tiro2 = Enemybullets('Assets/BossAttack.png',
                             self.rect.centerx,
                             self.rect.bottom, -vxt1)
        tiro3 = Enemybullets('Assets/BossAttack.png',
                             self.rect.centerx,
                             self.rect.bottom, vxt2)
        tiro4 = Enemybullets('Assets/BossAttack.png',
                             self.rect.centerx,
                             self.rect.bottom, -vxt2)
        tiro5 = Enemybullets('Assets/BossAttack.png',
                             self.rect.centerx,
                             self.rect.bottom, vxt3)
        tiro6 = Enemybullets('Assets/BossAttack.png',
                             self.rect.centerx,
                             self.rect.bottom, -vxt3)
        tudo.add(tiro)
        tudo.add(tiro1)
        tudo.add(tiro2)
        tudo.add(tiro3)
        tudo.add(tiro4)
        tudo.add(tiro5)
        tudo.add(tiro6)
        enemy_bullets.add(tiro)
        enemy_bullets.add(tiro1)
        enemy_bullets.add(tiro2)
        enemy_bullets.add(tiro3)
        enemy_bullets.add(tiro4)
        enemy_bullets.add(tiro5)
        enemy_bullets.add(tiro6)
        enemy_shoot_sound.play()
        
#===============================     Cores     ===============================#
GREEN = (0, 150, 0)
LIGHTGREEN = (0, 255, 0)
RED = (150, 0, 0)
LIGHTRED = (255, 0, 0)
BLUE = (0, 0, 150)
LIGHTBLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#================================     Som     ================================#
snd_dir = path.join(path.dirname (__file__), 'snd')
pygame.mixer.init()

#som do tiro do player
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser.wav'))

#som do tiro do inimigo
enemy_shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'EnemyLaser.wav'))

#sons da explosão
exp_sounds = []
for snd in ['Explosion1.wav', 'Explosion2.wav']:
    exp_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    
#sons dos powerups
pow_sounds = []
for snd in ['Pickup_Coin.wav', 'Pickup_Coin2.wav' ]:
    pow_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    
#som da morte
crash_sound = pygame.mixer.Sound(path.join(snd_dir, 'Crash.wav'))

#som nuke
nuke_sound = pygame.mixer.Sound(path.join(snd_dir, 'kaboom.wav'))

#som do boss
boss_sound = pygame.mixer.Sound(path.join(snd_dir, 'Alien.wav'))

musics = ['tgfcoder-FrozenJam-SeamlessLoop.ogg', 'Cosmic Storm.ogg',
          'SW.ogg', 'DV.ogg', 'boss.mp3']

def Musicas(mus):
    musica = musics[mus]
    pygame.mixer.music.load(path.join(snd_dir,
                                  musica))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops = -1)

#==============================     Funções     ==============================#  
def novo_meteoro(lista_meteoros, tudo, enemy_group):
    meteor = Meteoros(random.choice(lista_meteoros))
    tudo.add(meteor)
    enemy_group.add(meteor)
    
def novo_stalker(tudo, enemy_group, stalkers, alvo, boss_alive, lista_stalkers):
    if not boss_alive:
        stalker = Stalker(random.choice(lista_stalkers), alvo)
    else:
        stalker = Stalker('Assets/alien.gif', alvo)
    tudo.add(stalker)
    enemy_group.add(stalker)
    stalkers.add(stalker)
    
def novo_atirador(tudo, enemy_group, mobs, lista_atirador):
    mob = Atirador(random.choice(lista_atirador))
    tudo.add(mob)
    enemy_group.add(mob)
    mobs.add(mob)

def novo_boss(tudo, enemy_group, bosses):
    boss = Boss('Assets/Boss1.gif')
    tudo.add(boss)
    bosses.add(boss)

def shield(surf, x, y, pct, maximo, cor, w, h):
    if pct < 0:
        pct = 0
    BAR_LENGTH = w
    BAR_HEIGHT = h
    fill = (pct / maximo) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, cor, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    
def draw_nukes(surf, x, y, nukes, img):
    if nukes > 0:
        for i in range(nukes):
            img_rect = img.get_rect()
            img_rect.x = x + 35 * i
            img_rect.y = y
            surf.blit(img, img_rect)
    
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 35 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        
def draw_ship_options(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.centerx = x
    img_rect.centery = y
    surf.blit(img, img_rect)
    
def cronometro(value):
    valueD = (((value/365)/24)/60)

    valueH = (valueD)*365

    valueM = (valueH)*24

    valueS = (valueM)*60
    Seconds = int(valueS)
    
    return Seconds

def mensagem(mensagem, x, y, tamanho, COR):
   
    def textos(mensagem, fonte):
        textSurface = fonte.render(mensagem, True, COR)
        return textSurface, textSurface.get_rect()

    texto = pygame.font.SysFont('agencyfb', tamanho)
    TextSurf, TextRect = textos(mensagem, texto)
    TextRect.center = (x, y)
    tela.blit(TextSurf, TextRect)
        
def main():
    loop = True
    intro = True
    instruction = False
    Game = False
    while loop:
        x = 0
        mn = pygame.image.load("Assets/StarBackground.jpg").convert()
        Musicas(2)
        
        fundo = pygame.image.load("Assets/StarBackground.jpg").convert()
        
        lista_meteoros = ['Assets/asteroid.gif', 'Assets/meteor2_s.gif',
                                  'Assets/fire_meteor_xs.gif']
            
        lista_atirador = ['Assets/enemy_atirador.png',
                          'Assets/enemy_atirador2.png',
                          'Assets/enemy_atirador3.png']
        
        lista_stalkers = ['Assets/StalkerUFO.gif', 'Assets/Stalker3.gif']
        
        while intro:

            pressed_keys = pygame.key.get_pressed()
            
            if pressed_keys[pygame.K_ESCAPE]:
                Game = False
                escolha_nave = False
                intro = False
                instruction = False
                loop = False
                return
            if pressed_keys[pygame.K_RETURN]:
                Game = False
                escolha_nave = True
                intro = False
                instruction = False
            if pressed_keys[pygame.K_i]:
                Game = False
                escolha_nave = False
                intro = False
                instruction = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            #Movimento da tela na horintal da Tela de início 
            rel_x = x % mn.get_rect().width
            tela.blit(mn, (rel_x - mn.get_rect().width, 0))
            if rel_x < WIDTH:
                tela.blit(mn, (rel_x, 0))
            x += 2
            
            mensagem('GUARDIANS', WIDTH/2, HEIGHT/2 - 200, 130, YELLOW)
            mensagem('OF THE', WIDTH/2, HEIGHT/2 - 125, 30, YELLOW)
            mensagem('UNIVERSE', WIDTH/2, HEIGHT/2 - 50, 130, YELLOW)
            
            mensagem('Press Enter to Play', WIDTH/2, HEIGHT/2 + 50, 50,
                     LIGHTGREEN)
            mensagem('Press I for Instructions', WIDTH/2, HEIGHT/2 + 120, 50,
                     LIGHTBLUE)
            mensagem('Press ESC to Quit', WIDTH/2, HEIGHT/2 + 190, 50,
                     LIGHTRED)
            
            pygame.display.update()
            relogio.tick(FPS)
            
        x = 0
        inst = pygame.image.load("Assets/StarBackground.jpg").convert()
        
        while instruction:
            
            pressed_keys = pygame.key.get_pressed()
            
            if pressed_keys[pygame.K_RETURN]:
                Game = False
                escolha_nave = True
                intro = False
                instruction = False
            if pressed_keys[pygame.K_q]:
                Game = False
                intro = True
                instruction = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                    
            rel_x = x % inst.get_rect().width
            tela.blit(inst, (rel_x - inst.get_rect().width, 0))
            if rel_x < WIDTH:
                tela.blit(inst, (rel_x, 0))
            x -= 2
            
            mensagem('INSTRUCTIONS', WIDTH/2, HEIGHT/2 - 200, 130, WHITE)
            mensagem('Shoot: SPACE', WIDTH/2, HEIGHT/2 - 100, 50, WHITE)
            mensagem('Move: Arrow Keys', WIDTH/2, HEIGHT/2 - 50, 50, WHITE)
            mensagem('Pause: P',  WIDTH/2, HEIGHT/2, 50, WHITE)
            mensagem('NUKE!!!: C or V',  WIDTH/2, HEIGHT/2 + 50, 50, WHITE)

            
            mensagem('Press Q to go back to the Menu', WIDTH/2,
                     HEIGHT/2 + 170, 50, LIGHTRED)
            mensagem('Press Enter to Play', WIDTH/2, HEIGHT/2 + 100, 50, 
                  LIGHTGREEN)
            
            pygame.display.update()
            relogio.tick(FPS)
            
        y = 0
        img_escolha = pygame.image.load("Assets/StarBackground.jpg").convert()    
            
        while escolha_nave:
            
            with open ('highscore.txt', 'r') as file:
                if os.stat('highscore.txt').st_size == 0:
                    existe_highscore = False
                else:
                    existe_highscore = True
                    highscore = file.read()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            #Movimento da tela na horintal da escolha das naves 
            rel_y = y % img_escolha.get_rect().height
            tela.blit(img_escolha, (0, rel_y - img_escolha.get_rect().height))
            if rel_y < HEIGHT:
                tela.blit(img_escolha, (0, rel_y))
            y += 2
                    
            ship1 = 'Assets/MilleniumFalcon.png'
            
            img1 = pygame.image.load(ship1)
            image1 = pygame.transform.scale(img1, (150, 206))
            
            ship2 = 'Assets/X-Wing.png'
            
            img2 = pygame.image.load(ship2)
            image2 = pygame.transform.scale(img2, (150, 154))
            
            ship3 = 'Assets/USS_Defiant.png'
            
            img3 = pygame.image.load(ship3)
            image3 = pygame.transform.scale(img3, (150, 188))
        
            mensagem('PICK YOUR SHIP', WIDTH/2, 50, 100, YELLOW)    
            draw_ship_options(tela, WIDTH/2 - 250, HEIGHT/2, image1)
            mensagem('Millenium Falcon', WIDTH/2 - 250, HEIGHT/2 - 180, 30, WHITE)
            mensagem('Press 1', WIDTH/2 -250, HEIGHT/2 - 140, 30, WHITE)
            mensagem('Slow', WIDTH/2 -250, HEIGHT/2 + 125, 30, WHITE)
            mensagem('Heavy Shield', WIDTH/2 -250, HEIGHT/2 + 150, 30, WHITE)
            draw_ship_options(tela, WIDTH/2, HEIGHT/2, image2)
            mensagem('X-Wing', WIDTH/2, HEIGHT/2 - 180, 30, WHITE)
            mensagem('Press 2', WIDTH/2, HEIGHT/2 - 140, 30, WHITE)
            mensagem('Fast', WIDTH/2, HEIGHT/2 + 125, 30, WHITE)
            mensagem('Light Shield', WIDTH/2, HEIGHT/2 + 150, 30, WHITE)
            draw_ship_options(tela, WIDTH/2 + 250, HEIGHT/2, image3)
            mensagem('USS Defiant', WIDTH/2 + 250, HEIGHT/2 - 180, 30, WHITE)
            mensagem('Press 3', WIDTH/2 + 250, HEIGHT/2 - 140, 30, WHITE)
            mensagem('All-rounder', WIDTH/2 +250, HEIGHT/2 + 137.5, 30, WHITE)
            mensagem('Press Q to go back to the Menu', WIDTH/2, HEIGHT/2 + 250,
                     50, LIGHTRED)
            
            relogio.tick(FPS)
            pygame.display.update()
            
            pressed_keys = pygame.key.get_pressed()
            
            nave_group = pygame.sprite.Group()
            
            if pressed_keys[pygame.K_1]:
                pct_shield = 125
                nave = Nave(ship1, 4, pct_shield)
                nave_group.add(nave)
                boss_spawns = 0
                spawn_boss = False
                boss_alive = False
                escolha_nave = False
                intro = False
                Game = True
                instruction = False
                over = False
                start = time.time()
                tempo_pause = 0
                enemy_group = pygame.sprite.Group()
                bullets_group = pygame.sprite.Group()
                enemy_bullets = pygame.sprite.Group()
                powerups_group = pygame.sprite.Group()
                tudo = pygame.sprite.Group()
                vidas = pygame.sprite.Group()
                mobs = pygame.sprite.Group()
                stalkers = pygame.sprite.Group()
                
                boss = Boss('Assets/Boss1.gif')
                bosses = pygame.sprite.Group()
                tudo.add(bosses)
                
                img_tiros = 'Assets/tiro3.png'
                               
                for i in range(4):
                    novo_meteoro(lista_meteoros, tudo, enemy_group)
                
                tudo.add(stalkers)
                tudo.add(enemy_group)
                tudo.add(nave_group)
                tudo.add(vidas)
                
                score_tiros = 0
                score = 0
                y = 0
                Musicas(randrange(0,2))
                
            elif pressed_keys[pygame.K_2]:
                pct_shield = 75
                nave = Nave(ship2, 7.5, pct_shield)
                nave_group.add(nave)
                boss_spawns = 0
                spawn_boss = False
                boss_alive = False
                escolha_nave = False
                intro = False
                Game = True
                instruction = False
                over = False
                start = time.time()
                tempo_pause = 0
                enemy_group = pygame.sprite.Group()
                bullets_group = pygame.sprite.Group()
                enemy_bullets = pygame.sprite.Group()
                powerups_group = pygame.sprite.Group()
                tudo = pygame.sprite.Group()
                vidas = pygame.sprite.Group()
                mobs = pygame.sprite.Group()
                stalkers = pygame.sprite.Group()
                
                boss = Boss('Assets/Boss1.gif')
                bosses = pygame.sprite.Group()
                tudo.add(bosses)
                
                img_tiros = 'Assets/tiro1.png'
                                                
                for i in range(4):
                    novo_meteoro(lista_meteoros, tudo, enemy_group)
               
                tudo.add(stalkers)
                tudo.add(enemy_group)
                tudo.add(nave_group)
                tudo.add(vidas)
                
                score_tiros = 0
                score = 0
                y = 0
                Musicas(randrange(0,2))
                
            elif pressed_keys[pygame.K_3]:
                pct_shield = 100
                nave = Nave(ship3, 5, pct_shield)
                nave_group.add(nave)
                boss_spawns = 0
                spawn_boss = False
                boss_alive = False
                escolha_nave = False
                intro = False
                Game = True
                instruction = False
                over = False
                start = time.time()
                tempo_pause = 0
                enemy_group = pygame.sprite.Group()
                bullets_group = pygame.sprite.Group()
                enemy_bullets = pygame.sprite.Group()
                powerups_group = pygame.sprite.Group()
                tudo = pygame.sprite.Group()
                vidas = pygame.sprite.Group()
                mobs = pygame.sprite.Group()
                stalkers = pygame.sprite.Group()
                
                boss = Boss('Assets/Boss1.gif')
                bosses = pygame.sprite.Group()
                tudo.add(bosses)
                
                img_tiros = 'Assets/tiro2.png'

                for i in range(4):
                    novo_meteoro(lista_meteoros, tudo, enemy_group)
                
                tudo.add(stalkers)
                tudo.add(enemy_group)
                tudo.add(nave_group)
                tudo.add(vidas)
                
                score_tiros = 0
                score = 0
                y = 0
                Musicas(randrange(0,2))
                
            elif pressed_keys[pygame.K_q]:
                escolha_nave = False
                Game = False
                instruction = False
                over = False
                intro = True
                
        while Game:
            relogio.tick(FPS)
            agora = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:            
                    Game = False
                    loop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        nave.shoot(img_tiros, tudo, bullets_group)
                    elif event.key == pygame.K_v or event.key == pygame.K_c:
                        if nave.nukes > 0:
                            nave.nukes -= 1
                            nave.nuke(enemy_group, tudo, boss, boss_alive, 
                                      score, nave, stalkers,lista_meteoros,
                                      mobs, lista_atirador)
                            nuke_sound.play()

                    elif event.key == pygame.K_p:
                        pause = True
                        inicio_pause = time.time()
                        while pause:
                            
                            pressed_keys = pygame.key.get_pressed()
                        
                            if pressed_keys[pygame.K_q]:
                                Game = False
                                intro = True
                                instruction = False
                                pause = False
                            
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    return
                                if event.type == pygame.KEYDOWN:
                                    if event.key != pygame.K_q:
                                        fim_pause = time.time()
                                        tempo_pause = tempo_pause + fim_pause\
                                        - inicio_pause
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
            y += 5
            
            '''Inimigo bate na Nave'''
            hits = pygame.sprite.spritecollide\
            (nave, enemy_group, False, pygame.sprite.collide_circle)
            '''Tiro inimigo acerta a nave'''
            pipocos = pygame.sprite.groupcollide\
            (enemy_bullets, nave_group, True,
            False, pygame.sprite.collide_circle)
            '''Meteoro some ao bater na nave'''
            pygame.sprite.groupcollide\
            (enemy_group, nave_group, True,
            False, pygame.sprite.collide_circle)
            '''Nave acerta Boss'''
            danos = pygame.sprite.groupcollide\
            (bullets_group, bosses, True, False, pygame.sprite.collide_circle)
            
            for dano in danos:
                boss.shield -= dano.radius * 1
                expl = Explosion(dano.rect.center, 'bosstiro')
                tudo.add(expl)
                
                if boss.shield < 1:
                    death_explosion = Explosion(boss.rect.center, 'boss')
                    tudo.add(death_explosion)
                    boss.lives -= 1
                    boss.shield = 0
            
            if boss.lives == 0:
                boss.kill()
                boss_alive = False
                score += 1000
                Musicas(randrange(0, 2))
                boss.lives = 1
                    
            for hit in hits:
                crash_sound.play()
                nave.shield -= hit.radius * 1.5
                novo_meteoro(lista_meteoros, tudo, enemy_group)
                expl = Explosion(hit.rect.center, 'sm')
                tudo.add(expl)
                
                if nave.shield < 1 and nave.lives > 1:
                    death_explosion = Explosion(nave.rect.center, 'nave')
                    tudo.add(death_explosion)
                    nave.hide()
                    nave.lives -= 1
                    nave.shield = pct_shield
                    
                elif nave.shield < 1 and nave.lives == 1:
                    death_explosion = Explosion(nave.rect.center, 'nave')
                    tudo.add(death_explosion)
                    nave.hide()
                    nave.lives -= 1
                    nave.shield = 0
                    
            for pipoco in pipocos:
                crash_sound.play()
                nave.shield -= 50
                expl = Explosion(pipoco.rect.center, 'sm')
                tudo.add(expl)
                
                if nave.shield < 1:
                    death_explosion = Explosion(nave.rect.center, 'nave')
                    tudo.add(death_explosion)
                    nave.hide()
                    nave.lives -= 1
                    nave.shield = pct_shield
                    
                elif nave.shield < 1 and nave.lives == 1:
                    death_explosion = Explosion(nave.rect.center, 'nave')
                    tudo.add(death_explosion)
                    nave.hide()
                    nave.lives -= 1
                    nave.shield = 0
           
            if score >= (boss_spawns + 1) * 7500:
                spawn_boss = True
                boss_sound.play()
                Musicas(4)
                boss_spawns += 1     
                
            if nave.lives == 0:
                nave.kill()
            if nave.lives == 0 and not death_explosion.alive():
                Game = False
                spawn_boss = False
                Musicas(3)
                over = True
                x = 0

                go = pygame.image.load("Assets/StarBackground.jpg").convert()
                while over:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                        
                    pressed_keys = pygame.key.get_pressed()
                    
                    if pressed_keys[pygame.K_r]:
                        over = False
                        Game = True
                        loop = True
                        intro = False
                        instruction = False
                        boss_spawns = 0
                        spawn_boss = False
                        boss_alive = False
                        start = time.time()
                        tempo_pause = 0
                        nave.lives = 3
                        nave.nukes = 3
                        nave.shield = pct_shield
                        
                        enemy_group = pygame.sprite.Group()
                        nave_group = pygame.sprite.Group()
                        bullets_group = pygame.sprite.Group()
                        enemy_bullets = pygame.sprite.Group()
                        mobs = pygame.sprite.Group()
                        stalkers = pygame.sprite.Group()
                        tudo = pygame.sprite.Group()
                        fundo = pygame.image.load\
                        ("Assets/StarBackground.jpg").convert()
                        boss = Boss('Assets/Boss1.gif')
                        bosses = pygame.sprite.Group()
                        tudo.add(bosses)

                        nave_group.add(nave)

                        for i in range(4):
                            novo_meteoro(lista_meteoros, tudo, enemy_group)

                        tudo.add(enemy_group)
                        tudo.add(nave_group)
                        tudo.add(vidas)
                        Musicas(randrange(0,2))
                        score = 0
                        score_tiros = 0
                        
                        with open ('highscore.txt', 'r') as file:
                            if os.stat('highscore.txt').st_size == 0:
                                existe_highscore = False
                            else:
                                existe_highscore = True
                                highscore = file.read()

                    if pressed_keys[pygame.K_q]:
                        over = False
                        intro = True
                        instruction = False
                        Game = False
                        loop = True
                    
                    #Movimento da tela na horintal do Game Over 
                    rel_x = x % go.get_rect().width
                    tela.blit(go, (rel_x - go.get_rect().width, 0))
                    if rel_x < WIDTH:
                        tela.blit(go, (rel_x, 0))
                    x += 2
                    if not existe_highscore:
                        mensagem('GAME OVER', WIDTH/2, HEIGHT/2 - 150, 130, WHITE)
                        mensagem('Score: {0}'.format(score),
                                 WIDTH/2, HEIGHT/2 - 50, 50, YELLOW)
                        mensagem('Congratulations you have set a new highscore!',
                                 WIDTH/2,HEIGHT/2 + 25, 50,YELLOW)
                        mensagem('Press R to restart', WIDTH/2, HEIGHT/2 + 100,
                                     50, LIGHTGREEN)
                        mensagem('Press Q to go back to the Menu', WIDTH/2,
                                     HEIGHT/2 + 175, 50, LIGHTRED)
                        with open ('highscore.txt', 'w') as file:
                            file.write(str(score))
                        
                    elif existe_highscore and int(highscore) >= score:
                        mensagem('GAME OVER', WIDTH/2, HEIGHT/2 - 150, 130, WHITE)
                        mensagem('Score: {0}'.format(score),
                                 WIDTH/2, HEIGHT/2 - 50, 50, YELLOW)
                        mensagem('Highscore: {0}'.format(highscore), WIDTH/2,
                                 HEIGHT/2 + 25, 50, YELLOW)
                        mensagem('Press R to restart', WIDTH/2, HEIGHT/2 + 100,
                                     50, LIGHTGREEN)
                        mensagem('Press Q to go back to the Menu', WIDTH/2,
                                     HEIGHT/2 + 175, 50, LIGHTRED)
                    elif existe_highscore and int(highscore) < score:
                        mensagem('GAME OVER', WIDTH/2, HEIGHT/2 - 150, 130, WHITE)
                        mensagem('Score: {0}'.format(score),
                                 WIDTH/2, HEIGHT/2 - 50, 50, YELLOW)
                        mensagem('Congratulations! You have set a new highscore!',
                                 WIDTH/2,HEIGHT/2 + 25, 50,YELLOW)
                        mensagem('Press R to restart', WIDTH/2, HEIGHT/2 + 100,
                                     50, LIGHTGREEN)
                        mensagem('Press Q to go back to the Menu', WIDTH/2,
                                     HEIGHT/2 + 175, 50, LIGHTRED)
                        with open ('highscore.txt', 'w') as file:
                            file.write(str(score))
                    pygame.display.update()
                    relogio.tick(FPS)

            if Game:
                if boss_alive:
                    '''boss shield'''
                    shield(tela, WIDTH - 120, 20, boss.shield, 750, RED,\
                           100, 20)
                '''desenhando escudo'''
                shield(tela, 10, 50, nave.shield, pct_shield, GREEN, 100, 20)
                '''desenhando nukes'''
                draw_nukes(tela, 10, 80, nave.nukes, nuke)
                '''desenhando vidas'''
                draw_lives(tela, 10, 10, nave.lives, vida)
                '''Tiro da Nave acerta nos inimigos'''
                tiros = pygame.sprite.groupcollide\
                (enemy_group, bullets_group, True,
                True, pygame.sprite.collide_circle)

                for tiro in tiros:
                    if score < 1000:
                        novo_meteoro(lista_meteoros, tudo, enemy_group)
                        random.choice(exp_sounds).play()
                        expl = Explosion(tiro.rect.center, 'sm')
                        tudo.add(expl)
                    if score >= 1000 and score <= 2500:
                        randchoice_enemy = [1, 2]
                        resp = random.choice(randchoice_enemy)
                        if resp == 1:
                            novo_meteoro(lista_meteoros, tudo, enemy_group)
                            random.choice(exp_sounds).play()
                            expl = Explosion(tiro.rect.center, 'sm')
                            tudo.add(expl)
                        elif resp == 2:
                            novo_stalker(tudo, enemy_group, stalkers,
                                         nave, boss_alive, lista_stalkers)
                            random.choice(exp_sounds).play()
                            expl = Explosion(tiro.rect.center, 'lg')
                            tudo.add(expl)
                    if score >= 2500 and score <= 5000:
                        novo_atirador(tudo, enemy_group,
                                      mobs, lista_atirador)
                        random.choice(exp_sounds).play()
                        expl = Explosion(tiro.rect.center, 'lg')
                        tudo.add(expl)
                    if score > 5000:
                        randchoice_enemy = [1, 2, 3]
                        resp = random.choice(randchoice_enemy)
                        if resp == 1:
                            novo_meteoro(lista_meteoros, tudo, enemy_group)
                            random.choice(exp_sounds).play()
                            expl = Explosion(tiro.rect.center, 'sm')
                            tudo.add(expl)
                        elif resp == 2:
                            novo_stalker(tudo, enemy_group, stalkers,
                                         nave, boss_alive, lista_stalkers)
                            random.choice(exp_sounds).play()
                            expl = Explosion(tiro.rect.center, 'lg')
                            tudo.add(expl)
                        elif resp == 3:
                            novo_atirador(tudo, enemy_group,
                                      mobs, lista_atirador)
                            random.choice(exp_sounds).play()
                            expl = Explosion(tiro.rect.center, 'lg')
                            tudo.add(expl)
                    
                    #Soma um determinado valor ao score
                    score_tiros += 100 - tiro.radius
                    
                    #Chance de 10% de aparecerem powerups
                    if random.random() > 0.9:
                        pow = Pow(tiro.rect.center)
                        tudo.add(pow)
                        powerups_group.add(pow)
                
                #Gera um novo boss caso não haja um boss na tela e 
                #a pontuação necessária tenha sido atingida
                if spawn_boss and not boss_alive:
                    novo_boss(tudo, enemy_group, bosses)
                    random.choice(exp_sounds).play()
                    expl = Explosion(tiro.rect.center, 'bosstiro')
                    tudo.add(expl)
                    spawn_boss = False
                    boss_alive = True
                
                #Se houver mobs (atiradores) na tela, há uma chance de
                #cada um atirar
                for mob in mobs:
                    if randrange(1, 400) == 5:
                        mob.enemy_shoot(tudo, enemy_bullets)
                #Se o boss estiver na tela, possui uma chance de executar
                #a função de atirar
                for boss in bosses:
                    if randrange(1, 200) == 5:
                        boss.enemy_shoot(tudo, enemy_bullets)
                
                '''Nave pega powerup'''
                hits = pygame.sprite.spritecollide\
                (nave, powerups_group, True)
                for hit in hits:
                    #Nave recebe + shield
                    if hit.type == 'shield':
                        nave.shield += 20
                        if nave.shield >= pct_shield:
                            nave.shield = pct_shield
                            pow_sounds[1].play()
                    #Nave fica mais forte (+tiros)
                    if hit.type == 'gun':
                        nave.powerup()
                        pow_sounds[0].play()
                        
                #Desenha score na tela de jogo
                if score >= 0:
                    mensagem('{0}'.format(score), WIDTH/2, 20, 30, YELLOW)
                else:
                    mensagem('0', WIDTH/2, 20, 30, YELLOW)
                segundos_passados = cronometro(agora - start - tempo_pause)
                score_tempo = segundos_passados * 10
                score = score_tempo + score_tiros
                
                #Executa a função "update" de todas as classes
                tudo.update()
                #Desenha todos os sprites na tela
                tudo.draw(tela)
                #Atualiza o display
                pygame.display.update()
                
#==============================     Iniciar     ==============================#
pygame.init()
pygame.font.init()

WIDTH = 1000
HEIGHT = 600

tela = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('GOTU')

powerups_images = {}
powerups_images['shield'] = pygame.image.load("Assets/Shield.gif").convert()
powerups_images['gun'] = pygame.image.load("Assets/mis.gif").convert()

explosion = {}
explosion['lg'] = []
explosion['sm'] = []
explosion['nave'] = []
explosion['boss'] = []
explosion['bosstiro'] = []
for i in range(9):
    explo = 'Assets/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(explo).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (100, 100))
    explosion['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (75, 75))
    explosion['sm'].append(img_sm)
    img_nave = pygame.transform.scale(img, (150, 150))
    explosion['nave'].append(img_nave)
   
for i in range(1, 12):
    explo = 'Assets/BossExplosion{}.png'.format(i)
    img = pygame.image.load(explo).convert()
    img.set_colorkey(BLACK)
    img_boss = pygame.transform.scale(img, (300, 300))
    explosion['boss'].append(img_boss)
    img_bosstiro = pygame.transform.scale(img, (100, 100))
    explosion['bosstiro'].append(img_bosstiro)    
    
vida = pygame.image.load('Assets/Lives.png').convert()
img_nuke = pygame.image.load('Assets/Nuke.png').convert()
nuke = pygame.transform.scale(img_nuke, (30, 50 - 7))
nuke.set_colorkey(BLACK)

#===========================     Funcionamento     ===========================#
relogio =  pygame.time.Clock()
FPS = 120

main()
pygame.quit()