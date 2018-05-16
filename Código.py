# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:17:40 2018

Baseado no canal do Youtube KidsCanCode 
https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg

Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> 
licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
"""
import pygame
from random import randrange
import random
from os import path
import time

#==============================     Classes     ==============================#
class Nave(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width / 2) - 2
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 5
        self.vx = 0
        self.type = 'gun'
        self.power = 1
        
    def update(self):
        self.vx = 0
        self.vy = 0
        keystate = pygame.key.get_pressed()
        if self.power>=2 and pygame.time.get_ticks() - self.power_time > 3000:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
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
            
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        
    def shoot(self, tudo, bullets_group):
        if self.power == 1:
            tiro = Tiros('Assets/tiro1.png', self.rect.centerx, self.rect.top)
            tudo.add(tiro)
            bullets_group.add(tiro)
            shoot_sound.play()
        if self.power == 2:
            tiro1 = Tiros('Assets/tiro1.png', self.rect.left, self.rect.centery)
            tiro2 = Tiros('Assets/tiro1.png', self.rect.right, self.rect.centery)
            tudo.add(tiro1)
            tudo.add(tiro2)
            bullets_group.add(tiro1)
            bullets_group.add(tiro2)
            shoot_sound.play()
        if self.power >= 3:
            tiro1 = Tiros('Assets/tiro1.png', self.rect.left, self.rect.centery)
            tiro2 = Tiros('Assets/tiro1.png', self.rect.right, self.rect.centery)
            tiro3 = Tiros('Assets/tiro1.png', self.rect.centerx, self.rect.top)
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
        self.rect.x = randrange(0, 1000)
        self.rect.y = randrange(-150, -100)
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
            
class Vida(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem, dist_margem_direita):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.right = dist_margem_direita
        
class Atirador(pygame.sprite.Sprite):
    
        def __init__(self, arquivo_imagem):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(arquivo_imagem)
            self.rect = self.image.get_rect()
            self.radius = 56
            self.rect.y = randrange(-150, -100)
            self.rect.x = randrange(0, 1000)
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
    
#som da morte
crash_sound = pygame.mixer.Sound(path.join(snd_dir, 'Crash.wav'))

musics = ['tgfcoder-FrozenJam-SeamlessLoop.ogg', 'Cosmic Storm.ogg',
          'SW.ogg', 'DV.ogg']

def Musicas(mus):
    musica = musics[mus]
    pygame.mixer.music.load(path.join(snd_dir,
                                  musica))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops = -1)

#==============================     Funções     ==============================#  
def cronometro(value):
    valueD = (((value/365)/24)/60)

    valueH = (valueD)*365

    valueM = (valueH)*24

    valueS = (valueM)*60
    Seconds = int(valueS)
    
    valueMS = (valueS - valueS//1)*1000
    Miliseconds = int(valueMS)

    return Seconds, Miliseconds

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
        
def main():
    loop = True
    intro = True
    instruction = False
    Game = False
    while loop:
        x = 0
        mn = pygame.image.load("Assets/StarBackground.jpg").convert()
        Musicas(2)
        while intro:
            pressed_keys = pygame.key.get_pressed()
            
            if pressed_keys[pygame.K_ESCAPE]:
                Game = False
                intro = False
                instruction = False
                loop = False
                sair()
            if pressed_keys[pygame.K_RETURN]:
                Game = True
                intro = False
                instruction = False
                start = time.time()
                tempo_pause = 0
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
                Game = True
                intro = False
                instruction = False
                start = time.time()
                tempo_pause = 0
            if pressed_keys[pygame.K_q]:
                Game = False
                intro = True
                instruction = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
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
                     HEIGHT/2 + 170, 50, LIGHTRED)
            mensagem('Press Enter to Play', WIDTH/2, HEIGHT/2 + 100, 50, 
                  LIGHTGREEN)
            
            pygame.display.update()
            relogio.tick(FPS)
        
        enemy_group = pygame.sprite.Group()
        nave_group = pygame.sprite.Group()
        bullets_group = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        powerups_group = pygame.sprite.Group()
        tudo = pygame.sprite.Group()
        vidas = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
            
        fundo = pygame.image.load("Assets/StarBackground.jpg").convert()
        
        lista_naves = ['Assets/MilleniumFalcon.png', 'Assets/Galaga.png',
                       'Assets/X-Wing.png']
        
        nave = Nave(random.choice(lista_naves))
        nave_group.add(nave)
        
        vida1 = Vida('Assets/Lives.png', WIDTH - 10)
        vida2 = Vida('Assets/Lives.png', - vida1.rect.width + WIDTH - 20)
        vida3 = Vida('Assets/Lives.png', -2 * vida1.rect.width + WIDTH - 30)
        
        vidas.add(vida1, vida2, vida3)
        
        lista_meteoros = ['Assets/asteroid.gif', 'Assets/meteor2_s.gif',
                          'Assets/fire_meteor_xs.gif']
    
        for i in range(4):
            meteor = Meteoros(random.choice(lista_meteoros))
            tudo.add(meteor)
            enemy_group.add(meteor)
            
        tudo.add(enemy_group)
        tudo.add(nave_group)
        tudo.add(vidas)
        
        score_tiros = 0
        score = 0
        y = 0
        Musicas(randrange(0,2))
        fundo = pygame.image.load("Assets/StarBackground.jpg").convert()
        conta_vidas = 3
        
        while Game:
            relogio.tick(FPS)
            agora = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:            
                    Game = False
                    loop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        nave.shoot(tudo, bullets_group)
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
                                    pygame.quit()
                                    quit()
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
            y += 10
            
            '''Meteoro bate na Nave'''
            hits = pygame.sprite.spritecollide\
            (nave, enemy_group, False, pygame.sprite.collide_circle)
            '''Tiro inimigo acerta a nave'''
            pipoco = pygame.sprite.groupcollide\
            (enemy_bullets, nave_group, True,
            False, pygame.sprite.collide_circle)
            '''Meteoro some ao bater na nave'''
            pygame.sprite.groupcollide\
            (enemy_group, nave_group, True,
            False, pygame.sprite.collide_circle)
            
            if hits or pipoco:
                crash_sound.play()
                conta_vidas -= 1
                if conta_vidas == 2:
                    vida3.kill()
                elif conta_vidas == 1:
                    vida2.kill()
                else:
                    vida1.kill()
                    Game = False
                    Musicas(3)
                    over = True
                    x = 0
            
                    go = pygame.image.load("Assets/StarBackground.jpg").convert()
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
                            conta_vidas = 3
                            start = time.time()
                            tempo_pause = 0
                            
                            enemy_group = pygame.sprite.Group()
                            nave_group = pygame.sprite.Group()
                            bullets_group = pygame.sprite.Group()
                            mobs = pygame.sprite.Group()
                            tudo = pygame.sprite.Group()
                                
                            fundo = pygame.image.load\
                            ("Assets/StarBackground.jpg").convert()
                            
                            nave = Nave(random.choice(lista_naves))
                            nave_group.add(nave)
                            
                            vida1 = Vida('Assets/Lives.png', WIDTH - 10)
                            vida2 = Vida('Assets/Lives.png',
                                         -vida1.rect.width + WIDTH - 20)
                            vida3 = Vida('Assets/Lives.png',
                                         -2 * vida1.rect.width + WIDTH - 30)
                            
                            vidas.add(vida1, vida2, vida3)
                            
                            for i in range(4):
                                meteor = Meteoros(random.choice(lista_meteoros))
                                tudo.add(meteor)
                                enemy_group.add(meteor)
                                
                            tudo.add(enemy_group)
                            tudo.add(nave_group)
                            tudo.add(vidas)
                            Musicas(randrange(0,2))
                            score = 0
                            score_tiros = 0
                            
                        if pressed_keys[pygame.K_q]:
                            over = False
                            intro = True
                            instruction = False
                            Game = False
                            loop = True
                            
                        rel_x = x % go.get_rect().width
                        tela.blit(go, (rel_x - go.get_rect().width, 0))
                        if rel_x < WIDTH:
                            tela.blit(go, (rel_x, 0))
                        x += 2
                            
                        mensagem('GAME OVER', WIDTH/2, HEIGHT/2 - 100, 130,
                                 WHITE)
                        mensagem('Press R to restart', WIDTH/2, HEIGHT/2 + 10,
                                 50, LIGHTGREEN)
                        mensagem('Press Q to go back to the Menu', WIDTH/2,
                                 HEIGHT/2 + 100, 50, LIGHTRED)
                        
                        pygame.display.update()
                        relogio.tick(FPS)
            
            
            if Game:
                '''Tiro da Nave acerta nos inimigos'''
                tiros = pygame.sprite.groupcollide\
                (enemy_group, bullets_group, True,
                 True, pygame.sprite.collide_circle)
                
                for tiro in tiros:
                    if score < 100:
                        random.choice(exp_sounds).play()
                        meteor = Meteoros(random.choice(lista_meteoros))
                        tudo.add(meteor)
                        enemy_group.add(meteor)
                        expl = Explosion(tiro.rect.center, 'sm')
                        tudo.add(expl)
                    if score >= 100:
                        mob = Atirador('Assets/enemy_atirador.png')
                        tudo.add(mob)
                        enemy_group.add(mob)
                        mobs.add(mob)
                        expl = Explosion(tiro.rect.center, 'lg')
                        tudo.add(expl)
                    
                    score_tiros += 100 - tiro.radius
                    if random.random() > 0.8:
                        pow = Pow(tiro.rect.center)
                        tudo.add(pow)
                        powerups_group.add(pow)
                
                if score >= 100:
                    for mob in mobs:
                        if randrange(1, 200) == 5:
                            mob.enemy_shoot(tudo, enemy_bullets)
                
                hits = pygame.sprite.groupcollide\
                (nave_group, powerups_group, False, True)
                for hit in hits:
                    #if hit.type == 'shield':
                        
                    if hit.type == 'gun':
                        nave.powerup()
                
                if score >= 0:
                    mensagem('{0}'.format(score), WIDTH/2, 20, 30, YELLOW)
                else:
                    mensagem('0', WIDTH/2, 20, 30, YELLOW)
                segundos_passados = cronometro(agora - start - tempo_pause)[0]
                score_tempo = segundos_passados * 10
                score = score_tempo + score_tiros
                
                tudo.update()
                tudo.draw(tela)
                pygame.display.update()
                
#==============================     Iniciar     ==============================#
pygame.init()
pygame.font.init()

WIDTH = 1000
HEIGHT = 600

tela = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('2D Shooter')

powerups_images = {}
powerups_images['shield'] = pygame.image.load("Assets/Shield.gif").convert()
powerups_images['gun'] = pygame.image.load("Assets/mis.gif").convert()

explosion ={}
explosion['lg'] = []
explosion['sm'] = []
for i in range(9):
    explo = 'Assets/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(explo).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (100, 100))
    explosion['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (75, 75))
    explosion['sm'].append(img_sm)

#===========================     Funcionamento     ===========================#
relogio =  pygame.time.Clock()
FPS = 120

main()