import random
import pygame
from pygame.constants import QUIT , K_DOWN,K_UP,K_RIGHT,K_LEFT

pygame.init()

HIEGHT = 500
WIDTH = 700
COLOR_WHITE =(255,255,255)
color_black = (0,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)
FPS = pygame.time.Clock()


main_display =pygame.display.set_mode((WIDTH,HIEGHT))
PLAYER_SIZE = (20,20)
player = pygame.Surface(PLAYER_SIZE)
player.fill(COLOR_WHITE)
PLAYER_RECT =player.get_rect()
#player_speed =[1, 1]
player_move_down = [0,1]
player_move_right = [1, 0]
player_move_up = [0,-1]
player_move_left =[-1,0]

def create_enemy():
    enemy_size= (30,30)
    enemy = pygame.Surface(enemy_size)
    enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0,HIEGHT), *enemy_size)
    enemy_move = [random.randint (-6,-1), 0]
    return [enemy,enemy_rect,enemy_move]

def create_bonus():
    bonus_size= (40,40)
    bonus = pygame.Surface(bonus_size)
    bonus.fill(COLOR_GREEN)
    bonus_rect = pygame.Rect(random.randint(0,WIDTH),0, *bonus_size)
    bonus_move = [0,random.randint (1,3)]
    return [bonus,bonus_rect,bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)
enemis = []
bonusis = []

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
    
    main_display.fill(color_black)
    
    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and PLAYER_RECT.bottom < HIEGHT:
        PLAYER_RECT = PLAYER_RECT.move(player_move_down)
    
    if keys[K_RIGHT] and PLAYER_RECT.right < WIDTH:
        PLAYER_RECT = PLAYER_RECT.move(player_move_right)
    
    if keys[K_UP] and PLAYER_RECT.top < WIDTH:
        PLAYER_RECT = PLAYER_RECT.move(player_move_up)
    
    if keys[K_LEFT] and PLAYER_RECT.left < WIDTH:
        PLAYER_RECT = PLAYER_RECT.move(player_move_left)
    
    for enemy in enemis:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
    
    
    for bonus in bonusis:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
    
    #enemy_rect = enemy_rect.move(enemy_move)
    
    
    
    main_display.blit(player,PLAYER_RECT)
    
    #main_display.blit(enemy,enemy_rect)
    
    pygame.display.flip()
    
    for enemy in enemis:
        if enemy[1].left < 0 :
            enemis.pop(enemis.index(enemy))
            
    for bonus in bonusis:
        if bonus[1].top > HIEGHT :
            bonusis.pop(bonusis.index(bonus))