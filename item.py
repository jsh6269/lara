import pygame
from tool import *
import mouse
from glob import glob

item_possible = ['pot', 'torch', 'table', 'stove', 'dancer', 'gramophone']
item_set = []
item_pre = None

class item:
    item_block = []

    def __init__(self, name, x=win_size()[0]//2, y=win_size()[1]//2, prac=False, duration=4):
        self.name = name
        self.x, self.y = x, y
        image_path = sorted(glob('./item/{}*.png'.format(name)))
        self.images = [pygame.image.load(path) for path in image_path]
        if not image_path:
            image_path = sorted(glob('./item/{}*.gif'.format(name)))
            self.images = [rotozoom(pygame.image.load(path), 0, 1) for path in image_path]
        self.block_txt = './item_block/{}.txt'.format(name)
        self.corner_val = []
        self.prior = None
        self.frameCount, self.frame_duration = 0, duration
        self.real_corner = []
        if not prac:
            with open(self.block_txt, 'r') as f:
                for _ in range(4):
                    val = f.readline().split(' ')
                    self.corner_val.append((float(val[0]), float(val[1])))

                for _ in range(4):
                    val = f.readline().split(' ')
                    self.real_corner.append((float(val[0]), float(val[1])))

                pri = f.readline().split(' ')
                pri[0], pri[1] = float(pri[0]), float(pri[1])
                self.pri = pri[0], pri[1]

    def save(self, save_name):
        with open(save_name, 'a') as f:
            f.write('{}, {}, {}\n'.format(str(self.name), str(self.x), str(self.y)))

    def draw(self, win):
        self.frameCount = (self.frameCount + 1) % (self.frame_duration * len(self.images))
        win.blit(self.images[self.frameCount//self.frame_duration], (self.x, self.y))

    def designate_corner(self, girl):
        block = []
        for val2 in self.real_corner:
            if not is_in_rect(*get_room_corner(), (self.x + val2[0], self.y + val2[1])):
                return False
            for others in item_set:
                if is_in_rect(*others.real_corner, (self.x + val2[0], self.y + val2[1])):
                    return False

        for val in self.corner_val:
            # if not is_in_rect(*get_room_corner(), (self.pri[0] + self.x, self.pri[1] + self.y)):
            #     return False
            block.append([self.x + val[0], self.y + val[1]])

        if is_in_rect(*block, (girl.x, girl.y)):
            return False

        if self.name != 'dancer':
            item.item_block.append(block)

        self.prior = (self.pri[0] + self.x, self.pri[1] + self.y)
        self.real_corner = [(self.x + val2[0], self.y + val2[1]) for val2 in self.real_corner]
        return True


def experiment(event_lst, girl, win, it):
    a = item(it, prac=True)
    a.draw(win)
    block_txt = './item_block/{}.txt'.format(it)
    for event in event_lst:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                with open(block_txt, 'a') as f:
                    f.write(str(girl.x - a.x) + ' ' + str(girl.y - a.y)+'\n')
            if event.key == pygame.K_d:
                with open(block_txt, 'a') as f:
                    f.write(str(mouse_pos()[0] - a.x) + ' ' + str(mouse_pos()[1] - a.y)+'\n')
            if event.key == pygame.K_f:
                with open(block_txt, 'a') as f:
                    f.write(str(mouse_pos()[0] - a.x) + ' ' + str(mouse_pos()[1] - a.y)+'\n')


def get_item(name, x=None, y=None):
    if x is None or y is None:
        return item(name)
    else:
        return item(name, x, y)


def draw_request(win):
    global item_pre
    if item_pre is not None:
        item_pre.x, item_pre.y = - item_pre.pri[0] + mouse_pos()[0], - item_pre.pri[1] + mouse_pos()[1]
        item_pre.draw(win)



