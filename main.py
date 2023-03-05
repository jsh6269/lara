import pygame
from pygame.transform import rotozoom, flip

pygame.display.set_caption("Lara's room")
icon = pygame.image.load('./girl/icon.png')
pygame.display.set_icon(icon)

'''window와 background를 설정하는 코드'''
bg_mag = 1  # 배경 이미지를 몇 배 확대할 것인지 저장
win = pygame.display.set_mode((1190, 751), pygame.FULLSCREEN)
bg = rotozoom(pygame.image.load('./room/myRoom.PNG').convert(), 0, bg_mag)
win.fill((255, 255, 255))
win.blit(bg, (0, 0))

'''게임창 실행을 위한 기초 설정을 하는 코드'''
pygame.display.update()
pygame.mixer.init(buffer=128)
pygame.init()
clock = pygame.time.Clock()

from redraw import redraw
from hero import character
from tool import *
from mouse import *
from terminal import terminal
from interaction import interact

from item import *


'''게임화면 width, height 변수를 저장하는 코드'''
width, height = pygame.display.get_surface().get_size()

'''파라미터 : 캐릭터 배율, 초기 위치, 초기 이미지'''
chr_mag = 2.2
first_x, first_y = width//2, height//2
first_img = rotozoom(pygame.image.load('./girl/down1.png'), 0, chr_mag)

'''캐릭터의 모션이 담긴 이미지들을 불러오는 코드'''
up = [rotozoom(pygame.image.load('./girl/up{}.png'.format(i)), 0, chr_mag) for i in range(1, 5)]
down = [rotozoom(pygame.image.load('./girl/down{}.png'.format(i)), 0, chr_mag) for i in range(1, 5)]
left = [rotozoom(pygame.image.load('./girl/left{}.png'.format(i)), 0, chr_mag) for i in range(1, 5)]
right = [rotozoom(flip(pygame.image.load('./girl/left{}.png'.format(i)), True, False), 0, chr_mag) for i in range(1, 5)]
upLeft = [rotozoom(pygame.image.load('./girl/upLeft{}.png'.format(i)), 0, chr_mag) for i in range(1, 5)]
upRight = [rotozoom(flip(pygame.image.load('./girl/upLeft{}.png'.format(i)), True, False), 0, chr_mag) for i in range(1, 5)]
downLeft = [rotozoom(pygame.image.load('./girl/downLeft{}.png'.format(i)), 0, chr_mag) for i in range(1, 5)]
downRight = [rotozoom(flip(pygame.image.load('./girl/downLeft{}.png'.format(i)), True, False), 0, chr_mag) for i in range(1, 5)]
motion = {'up': up, 'down': down, 'left': left, 'right': right,
          'upLeft': upLeft, 'upRight': upRight, 'downLeft': downLeft, 'downRight': downRight}

'''마우스와 캐릭터의 위치관계에 따른 이동모션의 방향을 지정하는 코드'''
# 파라미터 uplr : left, right, up, down의 각도범위 반폭을 결정한다.
uplr_ang = 30 / 2
move_range = {
    'up_range': (90 - uplr_ang, 90 + uplr_ang),
    'down_range': (270 - uplr_ang, 270 + uplr_ang),
    'left_range': (180 - uplr_ang, 180 + uplr_ang),
    'right_range': (0, uplr_ang),
    'right_range2': (360 - uplr_ang, 360),
    'upLeft_range': (90 + uplr_ang, 180 - uplr_ang),
    'upRight_range': (uplr_ang, 90 - uplr_ang),
    'downLeft_range': (180 + uplr_ang, 270 - uplr_ang),
    'downRight_range': (270 + uplr_ang, 360 - uplr_ang)
}

# make terminal
ter = terminal()

# Lara를 만들고 등록한다.
girl = character(x=first_x, y=first_y, head='down', vel=4, img=first_img, order=False, dest_x=None,
                 dest_y=None, runCount=0, motion_data=motion, move_range_data=move_range, win=win)
girl_bar = rotozoom(pygame.image.load('./girl/Lara_bar.png'), 0, 0.35)

# # item enrollment
# pot = item('pot')


'''게임을 실행하는 코드'''
run = True

while run:
    clock.tick(48)
    event_lst = pygame.event.get()
    for event in event_lst:
        if event.type == pygame.QUIT:
            run = False

    girl.update(event_lst)
    redraw(win, bg, girl, girl_bar)
    a = ter.update(win, girl, event_lst)
    draw_request(win)
    # experiment(event_lst, girl, win, 'gramophone')
    interact(girl, event_lst, win)
    pygame.display.update()

    if a == 'fullscreen':
        win = pygame.display.set_mode((1190, 751), pygame.FULLSCREEN)
        pygame.display.set_caption("Lara's room")
        pygame.display.set_icon(icon)

    elif a == 'smallscreen':
        win = pygame.display.set_mode((1190, 751))
        pygame.display.set_caption("Lara's room")
        pygame.display.set_icon(icon)

pygame.quit()
