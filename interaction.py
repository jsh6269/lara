import pygame
from tool import *
import item
from glob import glob

rep_ang = {'up': 90, 'down': 270, 'left': 180, 'right': 0, 'upRight': 45, 'upLeft': 135, 'downLeft': 225, 'downRight': 315}


class music_player:
    def __init__(self):
        self.musics = sorted(glob('./music/*.mp3'))
        self.active = False
        self.number = 0

    def reset(self):
        self.active = False
        self.number = 0
        pygame.mixer_music.stop()

    def turn_off(self):
        global mess_counter
        self.active = False
        self.number = (self.number + 1) % len(self.musics)
        pygame.mixer_music.stop()
        mess_counter = 15

    def turn_on(self):
        global mess_counter
        self.active = True
        pygame.mixer_music.load(self.musics[self.number])
        pygame.mixer_music.play(-1)
        mess_counter = 15

    def manipulate(self):
        if self.active:
            self.turn_off()
        else:
            self.turn_on()


player = music_player()
font = pygame.font.Font('./terminal/SFMonoBold.otf', 15)
mess_counter = 0
on_text = font.render('music on', True, (0, 0, 0))
off_text = font.render('music off', True, (0, 0, 0))
pos = None


def interact(girl, event_lst, win):
    global mess_counter, pos
    if player.active and mess_counter != 0 and pos is not None:
        # on_text.set_alpha(int(255*mess_counter/15))
        win.blit(on_text, (pos[0]-30, pos[1]-80))
        mess_counter -= 1
    elif not player.active and mess_counter != 0 and pos is not None:
        # off_text.set_alpha(int(255*mess_counter/15))
        win.blit(off_text, (pos[0]-30, pos[1]-80))
        mess_counter -= 1

    for event in event_lst:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                name, pos = demand(girl)
                action(name, win)


def demand(girl):
    threshold = 60
    for stuff in item.item_set:
        if length(*stuff.prior, *girl.prior) < threshold and is_looking(girl, stuff):
            return stuff.name, stuff.prior
    return None, None


def is_looking(girl, stuff):
    ang = get_angle(*girl.prior, *stuff.prior)
    ang2 = rep_ang[girl.head]
    # print(ang, ang2)
    if abs(ang - ang2) < 50:
        return True
    if ang2 == 0 and abs(360 - ang) < 50:
        return True
    return False


def action(name, win):
    if name is None:
        return
    if name == 'gramophone':
        player.manipulate()
