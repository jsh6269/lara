import pygame
from pygame.transform import rotozoom, flip
import math
from mouse import *


def laser(x, y, win, color=(255, 0, 0)):
    # (x, y)에 레이저 포인터를 그려준다.
    x, y = int(x), int(y)
    # pygame.draw.circle(win, color, [x, y], 3, 2)
    

def is_in(x, y):
    # 입력받은 (x, y)가 화면 영역의 내부에 있는지 확인하는 함수
    width, height = pygame.display.get_surface().get_size()
    if 0 <= x <= width:
        if 0 <= y <= height:
            return True
    return False


def length(x, y, a, b):
    # (x, y)와 (a, b)의 길이를 구한다
    return ((x-a)**2 + (y-b)**2)**0.5


def get_angle(x, y, tx, ty):
    # (x, y)를 원점으로 하는 좌표계에서 (tx, ty)의 극좌표 상의 각도를 반환한다.
    # degree로 반환한다. 두 좌표가 일치하는 경우 None을 반환한다.
    r = length(x, y, tx, ty)
    if y == ty:
        if x < tx:
            return 0
        elif x > tx:
            return 180
        else:
            return None
    elif y > ty:
        # 0도와 180도 사이의 각도
        cos = (tx - x) / r
        return math.acos(cos) * 180 / math.pi

    elif y < ty:
        # 180도와 360도 사이의 각도
        cos = (tx - x) / r
        return 360 - (math.acos(cos) * 180 / math.pi)


def proj(vec1, vec2):
    # vec1을 vec2로 정사영한 벡터를 반환
    ab = vec1[0] * vec2[0] + vec1[1] * vec2[1]
    aa = vec2[0] * vec2[0] + vec2[1] * vec2[1]
    const = ab / aa
    return [vec2[0] * const, vec2[1] * const]


def intersect(m1, x1, y1, m2, x2, y2):
    # 기울기와 좌표로 정의되는 두 선분의 교점을 반환
    x = (m1 * x1 - y1 - m2 * x2 + y2) / (m1 - m2)
    y = m1 * (x - x1) + y1
    return x, y


def win_size():
    # 현재 창의 크기 width, height를 반환
    return pygame.display.get_surface().get_size()


def is_in_rect(p1, p2, p3, p4, p):
    # 점 p1, p2, p3, p4로 결정되는 볼록 사각형 내부에 점 p가 존재하는지 여부를 반환

    # y = a1 x + b1
    # y = a2 x + b2
    # y = a3 x + b3
    # y = a4 x + b4

    a1, b1 = get_coefficient(p1, p2)
    a2, b2 = get_coefficient(p3, p4)
    det1, det2 = p[1] - a1 * p[0] - b1, p[1] - a2 * p[0] - b2
    if det1 * det2 > 0:
        return False

    a3, b3 = get_coefficient(p1, p3)
    a4, b4 = get_coefficient(p2, p4)
    det3, det4 = p[1] - a3 * p[0] - b3, p[1] - a4 * p[0] - b4
    if det3 * det4 > 0:
        return False

    return True


def get_coefficient(pa, pb):
    # 점 pa, pb로 결정되는 선분의 기울기와 y절편을 반환
    m = (pa[1]-pb[1])/(pa[0]-pb[0])
    n = pa[1] - m * pa[0]
    return m, n


def get_room_corner():
    return [(676, 224), (1071, 420), (72, 529), (461, 726)]


def is_down(p, p1, p2):
    a, b = get_coefficient(p1, p2)
    # print(a, b, p1, p2)
    # print(p[1] < a * p[0] + b)
    return p[1] < a * p[0] + b


def press(event_lst, button):
    keys = pygame.key.get_pressed()
    if keys[button]:
        return True
    return False
    # for event in event_lst:
    #     if event.type == pygame.KEYUP:
    #         if event.key == button:
    #             return True
    # return False
