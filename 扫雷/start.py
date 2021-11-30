import pygame
from pygame.locals import *
from sys import exit
from json import load

from menu import Menu
from game import Game
from set import Set
from record import Record

pygame.init()
pygame.display.set_caption('扫雷')


class Sweeper(object):
    def __init__(self):
        self.size = [1920, 1080]
        self.screen = pygame.display.set_mode([100, 100], 0, 32)
        icon = pygame.image.load('images/mine1.png').convert_alpha()
        pygame.display.set_icon(icon)
        self.menu_screen = None
        self.game_screen = None
        self.set_screen = None
        self.record_screen = None
        self.alert_screen = None
        # 背景
        self.bg_1 = pygame.image.load('images/风景/1.jpg').convert()
        self.bg_2 = pygame.image.load('images/风景/2.jpg').convert()
        self.bg_3 = pygame.image.load('images/风景/3.jpg').convert()
        self.bg_4 = pygame.image.load('images/风景/4.jpg').convert()
        self.bg_5 = pygame.image.load('images/风景/5.jpg').convert()
        # 变量
        self.font = pygame.font.SysFont('kaiti', 15, False)
        self.now_screen = self.menu_screen
        self.now_bg = 0
        self.now_mine = 0
        self.now_flag = 0
        self.now_death = 0
        self.now_mark = 0
        self.init(update=True)

    # 根据配置文件初始化
    def init(self, update=False):
        config = load(open('config.json', 'r'))
        # 字体
        self.font = pygame.font.SysFont('kaiti', 40, False)
        # 窗口大小
        self.size = config[0]
        # 变量
        self.now_bg = int(config[2])
        self.now_mine = int(config[3])
        self.now_flag = int(config[4])
        self.now_death = int(config[5])
        self.now_mark = int(config[6])
        # 样式
        self.mine = pygame.image.load('images/mine%d.png' % (self.now_mine+1)).convert_alpha()
        self.flag = pygame.image.load('images/flag%d.png' % (self.now_flag+1)).convert_alpha()
        if update:
            self.screen = pygame.display.set_mode(self.size, int(config[1]), 32)
        self.menu_screen = Menu(self)
        self.game_screen = Game(self)
        self.set_screen = Set(self)
        self.record_screen = Record(self)
        self.now_screen = self.menu_screen
        # 背景
        self.bg_1_convert = pygame.transform.scale(pygame.image.load('images/风景/1.jpg').convert(), self.size)
        self.bg_2_convert = pygame.transform.scale(pygame.image.load('images/风景/2.jpg').convert(), self.size)
        self.bg_3_convert = pygame.transform.scale(pygame.image.load('images/风景/3.jpg').convert(), self.size)
        self.bg_4_convert = pygame.transform.scale(pygame.image.load('images/风景/4.jpg').convert(), self.size)
        self.bg_5_convert = pygame.transform.scale(pygame.image.load('images/风景/5.jpg').convert(), self.size)

    def start(self):
        while 1:
            # 先画背景
            self.screen.blit([self.bg_1_convert, self.bg_2_convert, self.bg_3_convert, self.bg_4_convert, self.bg_5_convert][self.now_bg], [0, 0])
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    exit()
                # 鼠标点击
                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.now_screen.click(pos, pygame.mouse.get_pressed().index(1))
                # 按键
                elif event.type == KEYDOWN:
                    key_press = pygame.key.get_pressed()
                    if key_press[K_LCTRL]:
                        self.game_screen.ai_speed += 1
                        if self.game_screen.ai_speed == 6:
                            self.game_screen.ai_speed = 0
                # 计时器
                else:
                    if self.now_screen == self.game_screen and event.type == self.game_screen.time_event:
                        self.game_screen.timer(event)
            # blit
            self.now_screen.blit()
            # hover
            pos = pygame.mouse.get_pos()
            self.now_screen.hover(pos)
            pygame.display.update()


game = Sweeper()
game.start()
