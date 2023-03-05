import pygame
from pygame.transform import rotozoom, flip
from tool import *
from mouse import *
from item import *

class character:
    def __init__(self, x, y, head, vel, img, order, dest_x, dest_y, runCount, motion_data, move_range_data, win):
        self.name = 'girl'
        self.x, self.y = x, y                       # 캐릭터의 (발 부근의) 좌표
        self.head = head                            # 캐릭터가 바라보는 방향
        self.vel = vel                              # 캐릭터의 이동속력
        self.img = img                              # 특정 순간의 캐릭터 이미지
        self.order = order                          # 캐릭터가 이동지시를 받아 이를 수행하고 있는지 여부를 저장하는 변수
        self.dest_x, self.dest_y = dest_x, dest_y   # 캐릭터가 이동지시를 받았을 경우 그 목적지 좌표
        self.runCount = runCount                    # 캐릭터가 움직일 때 몇 번째 sprite image의 frame인지 저장하는 변수
        self.motion = motion_data                   # 딕셔너리 데이터, {'left': [left에 해당하는 loaded sprite image], ... , so on}
        self.move_range = move_range_data           # 딕셔너리 데이터, {'up_range': (degree1, degree2), ...} degree1 ~ degree2 사이 각도에서는 up방향을 바라봄을 의미
        self.win = win                              # pygame window
        self.frame_duration = 6                     # Lara의 각 sprite image들이 몇 프레임동안 지속될 것인지 결정하는 변수
        self.ad_x, self.ad_y = -22, -80             # self.x, self.y의 위치와 캐릭터가 그려지는 위치 사이의 조화를 잡아주는 조정값
        self.block = None                           # 캐릭터가 방의 가장자리에 닿았는지, 닿았다면 어느 벽에 닿았는지 저장하는 변수
        self.freeze = False                         # terminal이 시작된 경우 일시 정지하도록 True로 저장, 아니면 False
        self.prior = (self.x + 2.2, self.y + 15)    # prior은 어떤 물체가 더 앞에 있는지 판단을 위한 변수. (가림 효과 고려). y좌표가 아래쪽을 향할 수록 다른 물체에 의해 가려지지 않게 그려져야한다
        self.real_corner = [(self.x-15, self.y), (self.x+15, self.y), (self.x - 15, self.y + 15), (self.x + 15, self.y + 15)]
        self.edge = {
            'left': [675-97, 228-526],
            'right': [1043-455, 422-714],
            'up': [1043-675, 422-228],
            'down': [455-97, 714-526]
        }

        # Lara의 방 좌표 및 가장자리 함수
        #               675, 228
        #                               y=0.527173913x -127.8423913
        #                                                                       1043, 422
        # y=-0.515571x+576.0104
        #
        #                                                    y=-0.49659864x + 939.952381
        # 97, 526
        #                    y=0.52514x+475.06142
        #                                                      455, 714

    def pause(self):
        self.freeze = True

    def resume(self):
        self.freeze = False

    def draw(self, win):
        win.blit(self.img, (self.x + self.ad_x, self.y + self.ad_y))
        # laser(*self.prior, win)
        # for pos in self.real_corner:
        #     laser(*pos, win)

    def stop(self):
        self.order = False
        self.dest_x, self.dest_y = None, None
        self.runCount = 0
        self.img = self.motion[self.head][0]

    def set_prior(self):
        self.prior = (self.x + 2.2, self.y + 15)
        self.real_corner = [(self.x-15, self.y), (self.x+15, self.y), (self.x - 15, self.y + 15), (self.x + 15, self.y + 15)]

    @staticmethod
    def is_outside(xx, yy):
        if -0.515571 * xx + 576.0104 < yy < -0.49659864 * xx + 939.952381:
            if 0.527173913 * xx -127.8423913 < yy < 0.52514 * xx + 475.06142:
                return False
        return True

    def is_block(self, xx, yy):
        if yy < -0.515571 * xx + 576.0104:
            self.block = 'left'
        elif yy > -0.49659864 * xx + 939.952381:
            self.block = 'right'
        elif yy < 0.527173913 * xx -127.8423913:
            self.block = 'up'
        elif yy > 0.52514 * xx + 475.06142:
            self.block = 'down'
        else:
            self.block = None

    @staticmethod
    def adjust_right_block(proj_vector):
        if proj_vector[0] > 0 and proj_vector[1] < 0:
            return length(0, 0, *proj_vector) > 45
        else:
            return length(0, 0, *proj_vector) > 2

    def go(self):
        if self.dest_x is None and self.dest_y is None and self.order:
            direction_way = {'left': math.pi, 'right': 0,
                             'down': 3 * math.pi / 2, 'up': math.pi / 2,
                             'upRight': math.pi / 4, 'upLeft': 3 * math.pi / 4,
                             'downLeft': 5 * math.pi / 4, 'downRight': 7 * math.pi/4}
            new_x, new_y = self.x + self.vel * math.cos(direction_way[self.head]), self.y + self.vel * math.sin(direction_way[self.head])
        else:
            dir = [self.dest_x - self.x, self.dest_y - self.y]
            size = length(0, 0, dir[0], dir[1])
            dir[0], dir[1] = dir[0] * self.vel / size, dir[1] * self.vel / size
            new_x, new_y = self.x + dir[0], self.y + dir[1]

        if any([is_in_rect(*stuff, [new_x, new_y]) for stuff in item.item_block]):
            self.stop()

        elif character.is_outside(new_x, new_y):
            if self.block is None:
                self.stop()
                self.is_block(new_x, new_y)
            else:
                out_vector = [self.dest_x - self.x, self.dest_y - self.y]
                proj_vector = proj(out_vector, self.edge[self.block])
                if (self.block != 'right' and length(0, 0, *proj_vector) > 5) or (self.block == 'right' and self.adjust_right_block(proj_vector)):
                    size = length(0, 0, proj_vector[0], proj_vector[1])
                    proj_vector[0], proj_vector[1] = proj_vector[0] * self.vel / 1.35 / size, proj_vector[1] * self.vel / 1.35 / size
                    new_x, new_y = self.x + proj_vector[0], self.y + proj_vector[1]
                    if not character.is_outside(new_x, new_y):
                        self.x, self.y = new_x, new_y
                    else:
                        self.stop()
                else:
                    self.stop()
        else:
            self.block = None
            self.x, self.y = new_x, new_y

    def update(self, event_lst):
        self.set_prior()

        if self.freeze:
            return

        buttons = [press(event_lst, keys) for keys in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]]

        # vel, order, destx, desty, head,   runCount, x, y, img
        # 마우스는 눌렀는데 너무 근거리에서 누른 경우
        if mouse_pressed() and length(self.x, self.y, *mouse_pos()) < 5:
            self.stop()

        # 가만히 있었는데 움직이도록 지시가 없는 경우
        elif not self.order and not mouse_pressed():
            pass

        # 가만히 있었는데 움직이도록 지시한 경우
        elif not self.order and mouse_pressed():
            angle = get_angle(self.x, self.y, *mouse_pos())
            if angle is not None:
                self.order = True
                self.dest_x, self.dest_y = mouse_pos()

                for key, val in self.move_range.items():
                    if val[0] <= angle <= val[1]:
                        self.head = key.split('_')[0]
                        break

                self.go()
                self.runCount = (self.runCount + 1) % (self.frame_duration * 4)
                img_number = self.runCount // self.frame_duration
                self.img = self.motion[self.head][img_number]

        # 움직이고 있었는데 지시가 없는 경우
        elif self.order and not mouse_pressed() and self.dest_x is not None:
            # 도착한 경우
            if length(self.x, self.y, self.dest_x, self.dest_y) < 5:
                self.order = False
                self.dest_x, self.dest_y = None, None
                self.runCount = 0
                self.img = self.motion[self.head][0]

            # 도착하지 않은 경우
            else:
                self.go()
                self.runCount = (self.runCount + 1) % (self.frame_duration * 4)
                img_number = self.runCount // self.frame_duration
                self.img = self.motion[self.head][img_number]

        # order, destx, desty, head, runCount, x, y,  img   vel.
        # 움직이고 있었는데 지시가 있는 경우
        elif self.order and mouse_pressed():
            self.dest_x, self.dest_y = mouse_pos()
            angle = get_angle(self.x, self.y, *mouse_pos())

            for key, val in self.move_range.items():
                if val[0] <= angle <= val[1]:
                    new_head = key.split('_')[0]
                    break

            if self.head == new_head:
                self.go()
                self.runCount = (self.runCount + 1) % (self.frame_duration * 4)
                img_number = self.runCount // self.frame_duration
                self.img = self.motion[self.head][img_number]

            else:
                self.runCount = 0
                self.go()
                self.head = new_head
                self.img = self.motion[self.head][0]

