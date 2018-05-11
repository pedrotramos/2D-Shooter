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
            
class Meteoros(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(arquivo_imagem).convert()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.x = randrange(0, 1200)
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
            self.rect.x = randrange(0, 1200)
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
            
class Vida(pygame.sprite.Sprite):
    
    def __init__(self, arquivo_imagem, dist_margem_direita):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.rect.top = 10
        self.rect.right = WIDTH - dist_margem_direita
    
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

musics = ['tgfcoder-FrozenJam-SeamlessLoop.ogg', 'Cosmic Storm.ogg',
          'SW.ogg', 'DV.ogg']

def Musicas(mus):
    musica = musics[mus]
    pygame.mixer.music.load(path.join(snd_dir,
                                  musica))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops = -1)

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
        
def main():
    loop = True
    intro = True
    instruction = False
    Game = False
    while loop:
        x = 0
        mn = pygame.image.load("Assets/SpaceBackground.png").convert()
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
            
            mensagem('Press Enter to Play', WIDTH/2, HEIGHT/2 + 20, 50,
                     LIGHTGREEN)
            mensagem('Press I for Instructions', WIDTH/2, HEIGHT/2 + 120, 50,
                     LIGHTBLUE)
            mensagem('Press ESC to Quit', WIDTH/2, HEIGHT/2 + 220, 50,
                     LIGHTRED)
            
            
            
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
        vidas = pygame.sprite.Group()
            
        fundo = pygame.image.load("Assets/SpaceBackground.png").convert()
        
        lista_naves = ['Assets/MilleniumFalcon.png', 'Assets/Galaga.png',
                       'Assets/X-Wing.png']
        
        nave = Nave(random.choice(lista_naves))
        nave_group.add(nave)
        
        vida1 = Vida('Assets/Lives.png', 10)
        vida2 = Vida('Assets/Lives.png', vida1.rect.width + 20)
        vida3 = Vida('Assets/Lives.png', 2 * vida1.rect.width + 30)
        
        vidas.add(vida1, vida2, vida3)
        
        lista_meteoros = ['Assets/asteroid.gif', 'Assets/meteor2_s.gif',
                          'Assets/fire_meteor_xs.gif']
    
        for i in range(8):
            meteor = Meteoros(random.choice(lista_meteoros))
            tudo.add(meteor)
            enemy_group.add(meteor)
            
        tudo.add(enemy_group)
        tudo.add(nave_group)
        tudo.add(vidas)
        
        score = 0
        y = 0
        Musicas(randrange(0,2))
        fundo = pygame.image.load("Assets/SpaceBackground.png").convert()
        conta_vidas = 3
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
                                    if event.key != pygame.K_q:
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
            pygame.sprite.groupcollide\
            (enemy_group, nave_group, True, False, pygame.sprite.collide_circle)
            if hits:
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
                            conta_vidas = 3
                            
                            enemy_group = pygame.sprite.Group()
                            nave_group = pygame.sprite.Group()
                            bullets_group = pygame.sprite.Group()
                            tudo = pygame.sprite.Group()
                                
                            fundo = pygame.image.load\
                            ("Assets/SpaceBackground.png").convert()
                            
                            nave = Nave(random.choice(lista_naves))
                            nave_group.add(nave)
                            
                            vida1 = Vida('Assets/Lives.png', 10)
                            vida2 = Vida('Assets/Lives.png',
                                         vida1.rect.width + 20)
                            vida3 = Vida('Assets/Lives.png',
                                         2 * vida1.rect.width + 30)
                            
                            vidas.add(vida1, vida2, vida3)
                            
                            for i in range(8):
                                meteor = Meteoros(random.choice(lista_meteoros))
                                tudo.add(meteor)
                                enemy_group.add(meteor)
                                
                            tudo.add(enemy_group)
                            tudo.add(nave_group)
                            tudo.add(vidas)
                            Musicas(randrange(0,2))
                            score = 0
                            
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
            
            tiros = pygame.sprite.groupcollide(enemy_group, bullets_group, True,
                                               True,
                                               pygame.sprite.collide_circle)
            for tiro in tiros:
                random.choice(exp_sounds).play()
                meteor = Meteoros(random.choice(lista_meteoros))
                tudo.add(meteor)
                enemy_group.add(meteor)        
                score += 100 - tiro.radius
            
            if Game:
                tudo.draw(tela)
                mensagem('{0}' .format(score), WIDTH/2, 20, 30, YELLOW)
                pygame.display.flip()
        
#===========================   'Iniciar'   ===========================#
pygame.init()
pygame.font.init()

WIDTH = 1000
HEIGHT = 600

tela = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('2D Shooter')


#===========================   'Funcionamento'   ===========================#
relogio =  pygame.time.Clock()
FPS = 120

main()