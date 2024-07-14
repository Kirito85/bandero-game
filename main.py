import random
import pygame
from pygame.constants import QUIT , K_DOWN,K_UP,K_RIGHT,K_LEFT
import os

pygame.init()

HIEGHT = 980
WIDTH = 1700

FONT = pygame.font.SysFont("Verdana",20)

COLOR_WHITE =(255,255,255)
color_black = (0,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)
FPS = pygame.time.Clock()

score = 0

main_display =pygame.display.set_mode((WIDTH,HIEGHT))

background = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH,HIEGHT))
bg_x1 = 0
bg_x2 = background.get_width()
bg_move = 3

image_path = "Goose"

PLAYER_IMAGES = os.listdir(image_path)


PLAYER_SIZE = (20,20)
player= pygame.image.load("player.png").convert_alpha()
PLAYER_RECT =player.get_rect()
PLAYER_RECT.center = main_display.get_rect().center
#player_speed =[1, 1]
player_move_down = [0,4]
player_move_right = [4, 0]
player_move_up = [0,-4]
player_move_left =[-4,0]

def create_enemy():
    enemy = pygame.image.load("enemy.png").convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, 
                             random.randint(enemy.get_height(),HIEGHT - enemy.get_height()), 
                             *enemy.get_size())
    enemy_move = [random.randint (-8,-4), 0]
    return [enemy,enemy_rect,enemy_move]

def create_bonus():
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus_width = bonus.get_width()
    bonus_rect = pygame.Rect(random.randint(bonus_width,WIDTH - bonus_width),
                            -bonus.get_height(), 
                            *bonus.get_size())
    bonus_move = [0,random.randint (4,8)]
    return [bonus,bonus_rect,bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT +3
pygame.time.set_timer(CHANGE_IMAGE, 200)



enemis = []
bonusis = []

image_index = 0

playing = True 

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemis.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonusis.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(image_path, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
    
    
    bg_x1 -= bg_move
    bg_x2 -= bg_move
    
    if bg_x1 < -background.get_width():
        bg_x1 = background.get_width()
        
    if bg_x2 < -background.get_width():
        bg_x2 = background.get_width()
    
    main_display.blit(background,(bg_x1,0))
    main_display.blit(background,(bg_x2,0))
    
    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and PLAYER_RECT.bottom < HIEGHT:
        PLAYER_RECT = PLAYER_RECT.move(player_move_down)
    
    if keys[K_RIGHT] and PLAYER_RECT.right < WIDTH:
        PLAYER_RECT = PLAYER_RECT.move(player_move_right)
    
    if keys[K_UP] and PLAYER_RECT.top > 0:
        PLAYER_RECT = PLAYER_RECT.move(player_move_up)
    
    if keys[K_LEFT] and PLAYER_RECT.left > 0:
        PLAYER_RECT = PLAYER_RECT.move(player_move_left)
    
    for enemy in enemis:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
    
        if PLAYER_RECT.colliderect(enemy[1]):
            playing = False
    
    
    for bonus in bonusis:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if PLAYER_RECT.colliderect(bonus[1]):
            score += 1
            bonusis.pop(bonusis.index(bonus))
    
    
    
    main_display.blit(FONT.render(str(score),True, color_black),(WIDTH-50, 20))
    main_display.blit(player,PLAYER_RECT)
    
    
    
    pygame.display.flip()
    
    for enemy in enemis:
        if enemy[1].right < 0 :
            enemis.pop(enemis.index(enemy))
            
    for bonus in bonusis:
        if bonus[1].top > HIEGHT :
            bonusis.pop(bonusis.index(bonus))