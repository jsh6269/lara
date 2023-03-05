import pygame
from tool import *
import mouse
import item
import os.path
import interaction

class terminal:
    set_item_mode = False

    def __init__(self):
        self.active = False
        self.new_order = False
        self.text = '>> '
        self.terminal_img = pygame.transform.rotozoom(pygame.image.load('./terminal/terminal.png'), 0, 1).convert()
        self.terminal_img.set_alpha(200)
        self.loc = (win_size()[0]//2-430, win_size()[1]//2-300)
        self.text_loc = (self.loc[0] + 20, self.loc[1] + 50)
        self.font = pygame.font.Font('./terminal/SFMonoBold.otf', 16)

    def check_power(self, girl, event_lst):
        for event in event_lst:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.active = not self.active
        if self.active:
            girl.pause()
            mouse.active = False
        else:
            girl.resume()
            mouse.active = True

    def get_text(self, event_lst):
        for event in event_lst:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.text.count('\n') <= 20 or self.text.endswith('>> clear'):
                        self.text = self.text + '\n'
                        self.new_order = True
                elif event.key == pygame.K_BACKSPACE:
                    if self.text[-3:] != '>> ':
                        self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, win, girl):
        win.blit(self.terminal_img, self.loc)
        self.text = self.text.replace('\t', '')

        message = self.text.split('\n')
        for i in range(len(message)):
            text_surface = self.font.render(message[i], True, (255, 255, 255))
            win.blit(text_surface, (self.text_loc[0], self.text_loc[1] + 25 * i))

    def operate(self, girl):
        if not self.new_order:
            return
        command = self.text.split('>> ')[-1][:-1]
        '''you should deal with the command here'''
        if command == 'clear':
            self.text = '>> '
        if command == 'quit game' or command == 'exit game':
            pygame.quit()
            exit()
        if command.startswith('get '):
            request_item = command[4:].strip()
            if request_item in item.item_possible:
                if item.item_pre is None:
                    req = item.get_item(request_item)
                    item.item_pre = req
                    # girl is already freezed
                    # mouse circle is freezed
                    mouse.freeze = True
                    # terminal should be closed
                    terminal.set_item_mode = True

        if command == 'remove all':
            item.item_set = []
            item.item.item_block = []
            interaction.player.reset()

        if command == 'help':
            self.text = self.text + 'command: get *, save *, load *, item, clear, help, remove all, quit game(exit game)\n'
            self.text = self.text + 'item available: ' + str(item.item_possible) + '\n'
            self.text = self.text + 'ex) get pot (click to place pot)' + '\n>> '

        if command == 'item':
            self.text = self.text + str(item.item_possible) + '\n>> '

        if command.startswith('save '):
            save_name = './save/' + command[5:].strip() + '.txt'
            with open(save_name, 'w') as f:
                f.write('{}, {}, {}\n'.format(girl.x, girl.y, girl.head))
            for stuff in item.item_set:
                stuff.save(save_name)

        if command.startswith('load '):
            load_name = './save/' + command[5:].strip() + '.txt'
            if os.path.isfile(load_name):
                interaction.player.reset()
                with open(load_name, 'r') as f:
                    lst = f.readline().split(', ')
                    girl.x, girl.y, girl.head = float(lst[0]), float(lst[1]), lst[2][:-1]
                    # girl.dest_x, girl.dest_y = None, None
                    # girl.order, girl.runCount = False, 0
                    girl.stop()
                    girl.set_prior()

                    lst2 = f.readlines()
                    new_obj = []
                    for line in lst2:
                        lst = line.split(', ')
                        stuff = item.item(lst[0], float(lst[1]), float(lst[2]))
                        stuff.designate_corner(girl)
                        new_obj.append(stuff)
                    item.item_set = new_obj

        print(command)
        self.new_order = False

        if command == 'fullscreen':
            return 'fullscreen'
        elif command == 'smallscreen':
            return 'smallscreen'

    def new_liner(self):
        if self.text[-1] == '\n':
            self.text += '>> '

    def update(self, win, girl, event_lst):
        if terminal.set_item_mode:
            if mouse_pressed():
                det_available = item.item_pre.designate_corner(girl)
                if not det_available:
                    return
                item.item_set.append(item.item_pre)
                item.item_pre = None
                mouse.freeze = False
                terminal.set_item_mode = False
            else:
                return

        self.check_power(girl, event_lst)
        if self.active:
            self.get_text(event_lst)
            a = self.operate(girl)
            self.new_liner()
            self.draw(win, girl)
            return a
