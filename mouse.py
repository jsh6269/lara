import pygame
import tool

mouse_pointer_lst = []
mouse_pointer_delay = 0
max_delay = 20
active = True
freeze = False


class mouse_pointer:
    def __init__(self, x, y, win, r=3, color=(205, 0, 89)):
        global mouse_pointer_delay
        self.color = color
        self.x = x
        self.y = y
        self.r = r
        self.width = 2
        self.maxR = 17
        self.max_duration = 1
        self.win = win
        mouse_pointer_delay = max_delay

    def draw(self):
        # 동심원 이펙트를 그리고 반지름을 증가시킨다
        draw_r = self.r if self.r < self.maxR else self.maxR
        pygame.draw.circle(self.win, self.color, [self.x, self.y], draw_r, self.width)
        if not freeze:
            self.r += 1

    def destroy(self):
        # 동심원이 사라져야할 시기가 되면 True를 반환한다
        if self.r > self.maxR + self.max_duration:
            return True
        return False


def manage_mouse_pointer(win):
    # 마우스를 클릭할 때 동심원이 퍼져나가는 이펙트가 정상적으로 작동하도록 관리한다

    global mouse_pointer_lst, mouse_pointer_delay
    del_lst = []

    if mouse_pointer_delay > 0:
        mouse_pointer_delay = mouse_pointer_delay - 1

    if not mouse_pressed():
        mouse_pointer_delay = 0

    if mouse_pressed() and mouse_pointer_delay == 0 and active:
        mouse_pointer_lst.append(mouse_pointer(*mouse_pos(), win))

    for i in range(len(mouse_pointer_lst)):
        cycle = mouse_pointer_lst[i]
        if cycle.destroy():
            del_lst.append(i)
        cycle.draw()

    for idx in del_lst:
        del mouse_pointer_lst[idx]


def mouse_pos():
    # 마우스의 위치를 반환한다.
    mouse = pygame.mouse.get_pos()
    return mouse[0], mouse[1]


def mouse_pressed():
    # 마우스가 눌려있는지 감지한다.
    # 마우스가 눌려있으면 True, 아니면 False 반환
    # assert tool.is_in(*mouse_pos())
    return pygame.mouse.get_pressed()[0]
