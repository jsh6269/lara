import pygame
from pygame.transform import rotozoom, flip
from tool import *
from mouse import *
import item
from functools import cmp_to_key


def check_posit(win, girl):
    # 마우스 포인터 (붉은색)
    # laser(*mouse_pos(), win)
    font = pygame.font.Font('Noto-Black.otf', 20)

    # 마우스와 캐릭터 좌표를 출력
    text = font.render("mouse: ({}, {})".format(*mouse_pos()), True, (230, 230, 230), (0, 0, 0))
    text2 = font.render("character: ({:.2f}, {:.2f})".format(girl.x, girl.y), True, (230, 230, 230), (0, 0, 0))
    win.blit(text, (50, 80))
    win.blit(text2, (50, 40))


def redraw(win, bg, girl, girl_bar):
    # 새로운 화면 출력을 위해 화면을 bg로 설정하여 지운다.
    win.blit(bg, (0, 0))
    laser(*mouse_pos(), win)

    # 마우스 위치를 체크하여 화면에 출력한다.
    # check_posit(win, girl)

    obj_lst = [girl] + item.item_set
    obj_lst.sort(key=cmp_to_key(pos_relation))
    for s2 in item.item_set:
        laser(*s2.real_corner[0], win)
        laser(*s2.real_corner[3], win)
    laser(*girl.prior, win)

    # obj_lst.sort(key=lambda s: s.prior[1])
    for obj in obj_lst:
        obj.draw(win)

    win.blit(girl_bar, (850, 600))
    # win.blit(cmd_bar, (50, 640))
    # 클릭할 때 나타나는 마우스 포인터를 그려준다
    manage_mouse_pointer(win)


def pos_relation(s1, s2):
    #                         s1.real_corner[1]
    # s1.real_corner[0]                   s1.real_corner[3]
    #                 s1.real_corner[2]
    # print(s1)
    if s2.name == 'girl':
        s1, s2 = s2, s1
        if is_down(s1.prior, s2.real_corner[0], s2.real_corner[3]):
            return 1
        else:
            return -1

    if is_down(s1.prior, s2.real_corner[0], s2.real_corner[3]):
        return -1
    else:
        return 1
