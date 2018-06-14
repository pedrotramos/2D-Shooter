# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:17:40 2018

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

As linhas que apresentarem '#' no final foram retiradas ou adaptadas
Baseado do canal do Youtube KidsCanCode 
https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
"""
# Bibliotecas necessárias
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
        self.power = 1 #
        self.power_time = pygame.time.get_ticks() #
        self.shield = shield # Valor de shield que o jogador possui
        self.lives = 3 # Número de vidas do jogador
        self.nukes = 3 # Número de bombas (Não há a chance de ganhar mais)
        self.hidden = False # Quando True tira a nave da tela
        self.hide_timer = pygame.time.get_ticks() # Duração do período escondido
        self.shoot_delay = 250 # Período entre tiros
        self.last_shot = pygame.time.get_ticks() # Guarda momento do último tiro
        
    def update(self, img_tiros, tudo, bullets_group):
        self.vx = 0
        self.vy = 0
        keystate = pygame.key.get_pressed()
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 5000:
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
        
        # Garante o Auto-fire
        if keystate[pygame.K_SPACE]:
            self.shoot(img_tiros, tudo, bullets_group)
        
        if self.lives > 1: #
            if self.hidden and pygame.time.get_ticks()\
            - self.hide_timer > 2000: #
                self.hidden = False #
            
    def powerup(self): # Aumenta o número de tiros da nave
        self.power += 1 # Aumenta as linhas de tiro em 1
        self.power_time = pygame.time.get_ticks() #
    
    # Explode todos os inimigos na tela e tira 200 de shield do boss
    def nuke(self, enemy_group, tudo, boss, boss_alive, score, nave, stalkers,
             lista_meteoros, mobs, lista_atirador, lista_stalkers):
        for enemy in enemy_group: # Explode inimigos
            expl = Explosion(enemy.rect.center, 'lg')
            enemy.kill()
            tudo.add(expl)
        if boss_alive: # Tira 200 de shield do boss
            boss_expl = Explosion(boss.rect.center, 'boss')
            boss.shield -= 200
            tudo.add(boss_expl)
            tudo.add()
        # Gera novos inimigos
        for i in range(4):
            if score < 1000:
                novo_meteoro(lista_meteoros, tudo, enemy_group)
            if score >= 1000 and score <= 2500:
                randchoice_enemy = [1, 2]
                resp = random.choice(randchoice_enemy)
                if resp == 1:
                    novo_meteoro(lista_meteoros, tudo, enemy_group)
                elif resp == 2:
                    novo_stalker(tudo, enemy_group, stalkers, nave, boss_alive, 
                                 lista_stalkers)
            if score >= 2500 and score <= 5000:
                novo_atirador(tudo, enemy_group, mobs, lista_atirador)
            if score > 5000:
                randchoice_enemy = [1, 2, 3]
                resp = random.choice(randchoice_enemy)
                if resp == 1:
                    novo_meteoro(lista_meteoros, tudo, enemy_group)
                elif resp == 2:
                    novo_stalker(tudo, enemy_group, stalkers, nave, boss_alive,
                                 lista_stalkers)
                elif resp == 3:
                    novo_atirador(tudo, enemy_group, mobs, lista_atirador)
    
    def hide(self): # Tira a nave da tela
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks() # Timer para voltar a aparecer
        self.rect.center = (WIDTH / 2, HEIGHT + 200) # Manda a nave de volta à sua origem
        
    def shoot(self, img_tiros, tudo, bullets_group): # Método atirar
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_delay: # Auto-fire
            self.last_shot = now
            if self.power == 1: # Para 1 linha de tiro
                # Define imagem e posição inicial da linha de tiro
                tiro = Tiros(img_tiros, self.rect.centerx, self.rect.top)
                tudo.add(tiro) # Adiciona o tiro ao grupo tudo
                bullets_group.add(tiro) # Adiciona o tiro ao grupo bullets_group
                shoot_sound.play() # Executa o som do tiro
            if self.power == 2: # Para 2 linhas de tiro
                tiro1 = Tiros(img_tiros, self.rect.left, self.rect.centery)
                tiro2 = Tiros(img_tiros, self.rect.right, self.rect.centery)
                tudo.add(tiro1)
                tudo.add(tiro2)
                bullets_group.add(tiro1)
                bullets_group.add(tiro2)
                shoot_sound.play()
            if self.power >= 3: # Para 3 linhas de tiro
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
        self.vy = -10 # Os tiros só se movem em y
        
    def update(self): # Move os tiros
        self.rect.y += self.vy
        if self.rect.bottom < 0: # Se o tiro sair da tela ele sai do jogo
            self.kill()
            
class Meteoros(pygame.sprite.Sprite): # Inimigos de tipo meteoro
    
    def __init__(self, arquivo_imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(arquivo_imagem).convert()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect() 
        self.radius = int(self.rect.width / 2) 
        self.rect.centerx = randrange(0, 1000) # Posição inicial em x do meteoro
        self.rect.centery = randrange(-100, -40) # Posição inicial em y do meteoro
        self.vy =  randrange(1, 7) # Velocidade em y do meteoro
        self.vx =  randrange(-3, 3) # Velocidade em x do meteoro
        self.rot = 0 #
        self.rot_speed = randrange(-8, 8) # Velocidade de rotação do meteoro
        self.last_update = pygame.time.get_ticks() #
        
    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        self.rotacao() # Rotaciona o meteoro
        if self.rect.top > HEIGHT or self.rect.right < 0 or \
        self.rect.left > WIDTH:
            self.rect.y = randrange(-100, -40) # Posição inicial em y do meteoro
            self.rect.x = randrange(0, 1000) # Posição inicial em x do meteoro
            self.vy = randrange(1, 7) # Velocidade em y do meteoro
            self.vx = randrange(-3,3) # Velocidade em x do meteoro
            
    def rotacao(self): # Rotaciona o meteoro
        tempo = pygame.time.get_ticks() #
        if tempo - self.last_update > 10: #
            self.last_update = tempo #
            self.rot = (self.rot + self.rot_speed) % 360 #
            new_image = pygame.transform.rotate(self.image_orig, self.rot) #
            old_center = self.rect.center #
            self.image = new_image #
            self.rect = self.image.get_rect() #
            self.rect.center = old_center #

class Explosion(pygame.sprite.Sprite): # Classe resposável pelas animações de explosão
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size # Define tamanho da explosão
        self.image = explosion[self.size][0] #
        self.rect = self.image.get_rect() #
        self.rect.center = center #
        self.frame = 0 #
        self.last_update = pygame.time.get_ticks() #
        self.frame_rate = 50 #

    def update(self): #
        now = pygame.time.get_ticks() #
        if now - self.last_update > self.frame_rate: #
            self.last_update = now #
            self.frame += 1 #
            if self.frame == len(explosion[self.size]):  #
                self.kill() #
            else: 
                center = self.rect.center #
                self.image = explosion[self.size][self.frame] #
                self.rect = self.image.get_rect() #
                self.rect.center = center #
                
class Nuke(pygame.sprite.Sprite):
    
    def __init__(self, center):
           self.image = 'Assets/Nuke.png' # Imagem do ícone Nuke
           self.rect = self.image.get_rect()
           self.rect.center = center

class Pow(pygame.sprite.Sprite):
    
    def __init__(self, center): 
        pygame.sprite.Sprite.__init__(self) 
        self.type = random.choice(['gun', 'shield']) # Escolhe 1 power-up aleatóriamente
        self.image = powerups_images[self.type] 
        self.rect = self.image.get_rect() 
        self.rect.center = center # Define posição inicial do power-up
        self.speedy = 2 # Velocidade em y do power-up
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill() # Tira o power-up do jogo

class Stalker(pygame.sprite.Sprite): # Inimigo que segue o jogador
    
    def __init__(self, arquivo_imagem, alvo):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(arquivo_imagem).convert()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.centery = randrange(-100, -40) # Posição inicial em y
        self.rect.centerx = randrange(0, 1000) # Posição inicial em x
        self.vy = 3 # Velocidade em y
        self.alvo = alvo # Define o alvo a ser perseguido
        self.rot = 0
        self.rot_speed = randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
    def update(self):
        # Checa posição em x em relação à posição em x do alvo
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
        self.rect.left > WIDTH: # Caso saia da tela
            self.rect.y = randrange(-100, -40) # Retorna ao x inicial
            self.rect.x = randrange(0, 1000) # Retorn ao y inicial
    
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
        self.rect.centery = randrange(-100, -40) # Posição inicial em y
        self.rect.centerx = randrange(0, 1000) # Posição inicial em x
        self.vy = 4 # Velocidade em y
        self.vx = randrange(-5,5,2) # Velocidade em x
            
    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if self.rect.right > WIDTH - 5: # Mudança de direção em x
            self.rect.right = WIDTH - 5
            self.vx = -self.vx
        if self.rect.left < 5:
            self.rect.left = 5
            self.vx = -self.vx
        if self.rect.bottom > 150: # Para de descer na altura de 150
            self.rect.bottom = 150
                
    def enemy_shoot(self, tudo, enemy_bullets): # Faz inimigo atirar
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

class Enemybullets(pygame.sprite.Sprite): # Gera tiro de inimigo
    def __init__(self, arquivo_imagem, pos_x, pos_y, vx):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem) # imagem do tiro
        self.rect = self.image.get_rect()
        self.rect.centery = pos_y # Posição y inicial
        self.rect.centerx = pos_x # Posição x inicial
        self.vy = 3 # Velocidade em y
        self.vx = vx # Velocidade em x
        
    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if self.rect.top > 600: # Tira tiro do jogo
            self.kill()

class Boss(pygame.sprite.Sprite): # Chefão do jogo
    def __init__(self, arquivo_imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.radius = 100 # Raio em que pode-se atingi-lo
        self.rect.centery = randrange(-150, -100) # Posição inicial em y
        self.rect.centerx = WIDTH / 2 # Posição inicial em x
        self.vy = 1 # Velocidade em y
        self.shield = 750 # Shield do chefão
        self.lives = 1 # Número de vidas do chefão
            
    def update(self):
        self.rect.y += self.vy
        if self.rect.bottom > 150: # Boss para quando chega a altura de 150
            self.rect.bottom = 150
        
    def enemy_shoot(self, tudo, enemy_bullets): # Gera 7 tiros para o boss
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
        enemy_shoot_sound.play() # Som de tiro
        
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
#Toda a parte de inserir som no jogo foi inspirada no canal do youtube.
#a função de Musicas foi feita pelo grupo para facilitar 
#a inserção das músicas tema no jogo
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
#Para não ficar repetindo as mesmas coisas durante o loop:
# Adiciona um novo meteoro ao jogo
def novo_meteoro(lista_meteoros, tudo, enemy_group):
    meteor = Meteoros(random.choice(lista_meteoros))
    tudo.add(meteor)
    enemy_group.add(meteor)

# Adiciona um novo stalker ao jogo   
def novo_stalker(tudo, enemy_group, stalkers, alvo, boss_alive, lista_stalkers):
    if not boss_alive:
        stalker = Stalker(random.choice(lista_stalkers), alvo)
    else:
        stalker = Stalker('Assets/alien.gif', alvo)
    tudo.add(stalker)
    enemy_group.add(stalker)
    stalkers.add(stalker)

# Adiciona um novo atirador ao jogo    
def novo_atirador(tudo, enemy_group, mobs, lista_atirador):
    mob = Atirador(random.choice(lista_atirador))
    tudo.add(mob)
    enemy_group.add(mob)
    mobs.add(mob)

# Adiciona um novo boss ao jogo
def novo_boss(tudo, enemy_group, bosses):
    boss = Boss('Assets/Boss1.gif')
    tudo.add(boss)
    bosses.add(boss)

# Desenha a barra de shield na tela
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

# Desenha os nukes na tela  
def draw_nukes(surf, x, y, nukes, img):
    if nukes > 0:
        for i in range(nukes):
            img_rect = img.get_rect()
            img_rect.x = x + 35 * i
            img_rect.y = y
            surf.blit(img, img_rect)

# Desenha as vidas na tela
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 35 * i
        img_rect.y = y
        surf.blit(img, img_rect)

# Desenha as opções de nave na tela de escolha        
def draw_ship_options(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.centerx = x
    img_rect.centery = y
    surf.blit(img, img_rect)

# Conta a passagem de segundos    
def cronometro(value):
    valueD = (((value/365)/24)/60)

    valueH = (valueD)*365

    valueM = (valueH)*24

    valueS = (valueM)*60
    Seconds = int(valueS)
    
    return Seconds

# Responsável pelas mensagens que aparecem no jogo
def mensagem(mensagem, x, y, tamanho, COR):
   
    def textos(mensagem, fonte):
        textSurface = fonte.render(mensagem, True, COR)
        return textSurface, textSurface.get_rect()

    texto = pygame.font.SysFont('agencyfb', tamanho)
    TextSurf, TextRect = textos(mensagem, texto)
    TextRect.center = (x, y)
    tela.blit(TextSurf, TextRect)

# Loop principal        
def main():
    # Variáveis que definem a tela que será exibida
    loop = True
    intro = True
    instruction = False
    Game = False
    while loop:
        x = 0
        mn = pygame.image.load("Assets/StarBackground.jpg").convert() # Imagem de fundo
        Musicas(2) # Música do menu
        
        fundo = pygame.image.load("Assets/StarBackground.jpg").convert() # Imagem de fundo
        
        lista_meteoros = ['Assets/asteroid.gif', 'Assets/meteor2_s.gif',
                                  'Assets/fire_meteor_xs.gif'] # Lista de imagens de meteoros
            
        lista_atirador = ['Assets/enemy_atirador.png',
                          'Assets/enemy_atirador2.png',
                          'Assets/enemy_atirador3.png'] # Lista de imagens de atiradores
        
        lista_stalkers = ['Assets/StalkerUFO.gif', 'Assets/Stalker3.gif'] # Lista de imagens de stalkers
        
        while intro: # Menu inicial

            pressed_keys = pygame.key.get_pressed()
            
            if pressed_keys[pygame.K_ESCAPE]: # Sair do jogo
                Game = False
                escolha_nave = False
                intro = False
                instruction = False
                loop = False
                return
            if pressed_keys[pygame.K_RETURN]: # Jogar
                Game = False
                escolha_nave = True
                intro = False
                instruction = False
            if pressed_keys[pygame.K_i]: # Instruções
                Game = False
                escolha_nave = False
                intro = False
                instruction = True
            
            for event in pygame.event.get(): # Sair caso clique no X da janela
                if event.type == pygame.QUIT:
                    return
            
            #Movimento da tela na horintal da Tela de início 
            rel_x = x % mn.get_rect().width
            tela.blit(mn, (rel_x - mn.get_rect().width, 0))
            if rel_x < WIDTH:
                tela.blit(mn, (rel_x, 0))
            x += 2
            
            # Textoa do Menu inicial
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
        
        while instruction: # Tela de instruções
            
            pressed_keys = pygame.key.get_pressed()
            
            if pressed_keys[pygame.K_RETURN]: # Jogar
                Game = False
                escolha_nave = True
                intro = False
                instruction = False
            if pressed_keys[pygame.K_q]: # Voltar ao Menu inicial
                Game = False
                intro = True
                instruction = False
            
            for event in pygame.event.get(): # Sair do jogo caso clique o X da janela
                if event.type == pygame.QUIT:
                    return
            
            # Movimento Horizontal da tela de instruções
            rel_x = x % inst.get_rect().width
            tela.blit(inst, (rel_x - inst.get_rect().width, 0))
            if rel_x < WIDTH:
                tela.blit(inst, (rel_x, 0))
            x -= 2
            
            # Textos da tela de instruções
            mensagem('INSTRUCTIONS', WIDTH/2, HEIGHT/2 - 200, 130, WHITE)
            mensagem('Shoot: SPACE', WIDTH/2, HEIGHT/2 - 100, 50, WHITE)
            mensagem('Move: Arrow Keys', WIDTH/2, HEIGHT/2 - 50, 50, WHITE)
            mensagem('Pause: P',  WIDTH/2, HEIGHT/2, 50, WHITE)
            mensagem('NUKE!!!: B',  WIDTH/2, HEIGHT/2 + 50, 50, WHITE)

            
            mensagem('Press Q to go back to the Menu', WIDTH/2,
                     HEIGHT/2 + 170, 50, LIGHTRED)
            mensagem('Press Enter to Play', WIDTH/2, HEIGHT/2 + 100, 50, 
                  LIGHTGREEN)
            
            pygame.display.update()
            relogio.tick(FPS)
            
        y = 0
        img_escolha = pygame.image.load("Assets/StarBackground.jpg").convert()    
            
        while escolha_nave: # Tela de escolha de nave
            
            # Abre o arquivo highscore e identifica o recorde atual
            with open ('highscore.txt', 'r') as file:
                if os.stat('highscore.txt').st_size == 0:
                    existe_highscore = False
                else:
                    existe_highscore = True
                    highscore = file.read()
            
            for event in pygame.event.get(): # Sai do jogo caso o X da janela seja clicado
                if event.type == pygame.QUIT:
                    return
            
            #Movimento da tela na vertical da escolha da nave
            rel_y = y % img_escolha.get_rect().height
            tela.blit(img_escolha, (0, rel_y - img_escolha.get_rect().height))
            if rel_y < HEIGHT:
                tela.blit(img_escolha, (0, rel_y))
            y += 2
            
            # Define as imagens a serem exibidas
            ship1 = 'Assets/MilleniumFalcon.png'
            
            img1 = pygame.image.load(ship1)
            image1 = pygame.transform.scale(img1, (150, 206))
            
            ship2 = 'Assets/X-Wing.png'
            
            img2 = pygame.image.load(ship2)
            image2 = pygame.transform.scale(img2, (150, 154))
            
            ship3 = 'Assets/USS_Defiant.png'
            
            img3 = pygame.image.load(ship3)
            image3 = pygame.transform.scale(img3, (150, 188))
            
            # Exibe mensagens e imagens das naves
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
            
            if pressed_keys[pygame.K_1]: # Escolhe a Millenium Falcon
                # Define todas as variáveis necessárias para que o jogo seja iniciado
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
                tudo.add(vidas)
                
                score_tiros = 0
                score = 0
                y = 0
                Musicas(randrange(0,2))
                
            elif pressed_keys[pygame.K_2]: # Escolhe a X-Wing
                # Define todas as variáveis necessárias para que o jogo seja iniciado
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
                tudo.add(vidas)
                
                score_tiros = 0
                score = 0
                y = 0
                Musicas(randrange(0,2))
                
            elif pressed_keys[pygame.K_3]: # Escolhe a USS Defiant
                # Define todas as variáveis necessárias para que o jogo seja iniciado
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
                tudo.add(vidas)
                
                score_tiros = 0
                score = 0
                y = 0
                Musicas(randrange(0,2))
                
            elif pressed_keys[pygame.K_q]: # Retorna ao Menu inicial
                escolha_nave = False
                Game = False
                instruction = False
                over = False
                intro = True
                
        while Game: # Loop do jogo
            relogio.tick(FPS)
            agora = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Sai do jogo se o X da janela for clicado            
                    Game = False
                    loop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b: # Usa o nuke
                        if nave.nukes > 0:
                            nave.nukes -= 1 # Perde um nuke
                            nave.nuke(enemy_group, tudo, boss, boss_alive, 
                                      score, nave, stalkers,lista_meteoros,
                                      mobs, lista_atirador, lista_stalkers)
                            nuke_sound.play() # Toca o som "Kaboom"

                    elif event.key == pygame.K_p: # Pausa o jogo
                        pause = True
                        inicio_pause = time.time()
                        while pause: # Tela de pause
                            
                            pressed_keys = pygame.key.get_pressed()
                        
                            if pressed_keys[pygame.K_q]: # Volta ao Menu inicial
                                Game = False
                                intro = True
                                instruction = False
                                pause = False
                            
                            for event in pygame.event.get(): # Sai do jogo caso o X da janela seja clicado
                                if event.type == pygame.QUIT:
                                    return
                                if event.type == pygame.KEYDOWN:
                                    # Volta pro jogo caso uma tecla sem ser Q seja clicada
                                    if event.key != pygame.K_q:
                                        fim_pause = time.time()
                                        tempo_pause = tempo_pause + fim_pause\
                                        - inicio_pause # Desconta o tempo pausado dos pontos ganhos por tempo jogado
                                        pause = False
                                        
                            # Textos da tela de pause            
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
            '''Nave bate no Boss'''
            boss_hits = pygame.sprite.spritecollide\
            (nave, bosses, False, pygame.sprite.collide_circle)
            '''Tiro inimigo acerta a nave'''
            pipocos = pygame.sprite.groupcollide\
            (enemy_bullets, nave_group, True,
            False, pygame.sprite.collide_circle)
            '''Meteoro some ao bater na nave'''
            pygame.sprite.groupcollide\
            (enemy_group, nave_group, True,
            False, pygame.sprite.collide_circle)
            '''Tiro da nave acerta Boss'''
            danos = pygame.sprite.groupcollide\
            (bullets_group, bosses, True, False, pygame.sprite.collide_circle)
            
            # A cada hit no boss
            for dano in danos:
                boss.shield -= dano.radius * 1
                expl = Explosion(dano.rect.center, 'bosstiro')
                tudo.add(expl)
                
                # Boss explode caso perca todo seu shield
                if boss.shield < 1:
                    death_explosion = Explosion(boss.rect.center, 'boss')
                    tudo.add(death_explosion)
                    boss.lives -= 1
                    boss.shield = 0
            
            # Consequências da morte do boss
            if boss.lives == 0:
                boss.kill()
                boss_alive = False
                score += 1000
                Musicas(randrange(0, 2))
                boss.lives = 1
                    
            for hit in hits: # A cada choque entre nave e inimigo
                crash_sound.play() # Som de batida
                nave.shield -= hit.radius * 1.5 # Nave perde shield
                novo_meteoro(lista_meteoros, tudo, enemy_group) # Novo meteoro surge
                expl = Explosion(hit.rect.center, 'sm') # Animação de explosão
                tudo.add(expl)
                
                # Nave perdendo vida
                if nave.shield < 1 and nave.lives > 1:
                    death_explosion = Explosion(nave.rect.center, 'nave')
                    tudo.add(death_explosion)
                    nave.hide()
                    nave.lives -= 1
                    nave.shield = pct_shield
                
                # Nave perdendo a última vida
                elif nave.shield < 1 and nave.lives == 1:
                    death_explosion = Explosion(nave.rect.center, 'nave')
                    tudo.add(death_explosion)
                    nave.hide()
                    nave.lives -= 1
                    nave.shield = 0
            
            # Nave se choca com o boss
            for boss_hit in boss_hits:
                crash_sound.play()
                nave.shield = 0 # Nave perde todo seu shield
                boss.shield -= 100 # Boss perde 100 de shield
                death_explosion = Explosion(nave.rect.center, 'nave')
                tudo.add(death_explosion)
                nave.hide()
                if nave.lives > 1:
                    nave.lives -= 1
                    nave.shield = pct_shield
                elif nave.lives == 1:
                    nave.lives -= 1
                    nave.shield = 0
            
            # A cada tiro que acerta a nave
            for pipoco in pipocos:
                crash_sound.play()
                nave.shield -= 50 # Nave perde 50 de shield
                expl = Explosion(pipoco.rect.center, 'sm') # Explosão acontece
                tudo.add(expl)
                
                # NAve perdendo vida
                if nave.shield < 1:
                    death_explosion = Explosion(nave.rect.center, 'nave')
                    tudo.add(death_explosion)
                    nave.hide()
                    nave.lives -= 1
                    nave.shield = pct_shield
                 
                # Nave perdendo a última vida    
                elif nave.shield < 1 and nave.lives == 1:
                    death_explosion = Explosion(nave.rect.center, 'nave')
                    tudo.add(death_explosion)
                    nave.hide()
                    nave.lives -= 1
                    nave.shield = 0
           
            # Define quando o boss deve aparecer
            if score >= (boss_spawns + 1) * 7500:
                spawn_boss = True
                boss_sound.play()
                Musicas(4)
                boss_spawns += 1     
            
            # Some com a nave caso não haja mais vidas
            if nave.lives == 0:
                nave.kill()
            if nave.lives == 0 and not death_explosion.alive():
                Game = False
                spawn_boss = False
                Musicas(3)
                over = True
                x = 0

                go = pygame.image.load("Assets/StarBackground.jpg").convert()
                while over: # Tela de Game Over
                    for event in pygame.event.get(): # Sai do jogo caso o X da janela seja clicado
                        if event.type == pygame.QUIT:
                            return
                        
                    pressed_keys = pygame.key.get_pressed()
                    
                    if pressed_keys[pygame.K_r]: # Recomeça o jogo
                        # Define varáveis para o que o jogo seja recomeçado
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
                        tudo.add(vidas)
                        Musicas(randrange(0,2))
                        score = 0
                        score_tiros = 0
                        
                        # Encontra o valor atual de highscore
                        with open ('highscore.txt', 'r') as file:
                            if os.stat('highscore.txt').st_size == 0:
                                existe_highscore = False
                            else:
                                existe_highscore = True
                                highscore = file.read()

                    if pressed_keys[pygame.K_q]: # Retorna ao menu inicial
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
                    
                    # Caso não exista um highscore
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
                    
                    # Caso o highscore atual seja maior que a pontuação do jogador
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
                    
                    # Caso o highscore atual seja menor que a pontuação do jogador
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
                        # Guarda no arquivo highscore.txt o novo highscore
                        with open ('highscore.txt', 'w') as file:
                            file.write(str(score))
                    pygame.display.update()
                    relogio.tick(FPS)

            if Game: # Se estiver no jogo
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

                for tiro in tiros: # Para cada hit nos inimigos
                    # Define tipo de inimigo que deverá aparecer
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
                nave_group.update(img_tiros, tudo, bullets_group)
                #Desenha todos os sprites na tela
                tudo.draw(tela)
                nave_group.draw(tela)
                #Atualiza o display
                pygame.display.update()
                
#==============================     Iniciar     ==============================#
pygame.init()
pygame.font.init()

WIDTH = 1000
HEIGHT = 600

tela = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('GOTU')

#Explosões lm e sm baseadas no canal do youtube. Demais, adaptadas para o 
#nosso jogo 

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
img_logo = pygame.image.load('Assets/Logo.png')
logo = pygame.transform.scale(img_logo, (100, 100))
pygame.display.set_icon(logo)

#===========================     Funcionamento     ===========================#
relogio =  pygame.time.Clock()
FPS = 120

main()
pygame.quit()