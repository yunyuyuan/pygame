import pygame
from pygame.locals import *
from 小工具.gametool.alert import Window
from sys import exit

from menu import Menu
from play import Play
from set import Set
from room import Room
from record import Record


pygame.init()
pygame.mouse.set_cursor(*pygame.cursors.tri_left)


class Game(object):
    def __init__(self, server, num):
        self.screen = pygame.display.set_mode([1920, 1080], FULLSCREEN, 32)
        # 主背景
        self.bg = pygame.image.load('./images/bg.jpg').convert()
        # 服务器ip
        self.server_ip = server
        # 用户id
        self.user_num = num
        # 初始化几个界面
        self.menu_screen = Menu(self.screen)
        self.play_screen = Play(self, self.screen)
        self.set_screen = Set(self, self.screen)
        self.room_screen = Room(self, self.screen)
        self.record_screen = Record(self, self.screen)
        # 打开软件时默认在菜单界面
        self.now_screen = 'menu'
        # 弹窗的类型
        self.alert_window = None
        self.alert_mod = '0'

    def began(self):
        while 1:
            # 首先显示背景
            self.screen.blit(self.bg, [0, 0])
            # 事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    exit()
                # 计时事件
                if self.alert_window:
                    if self.alert_window.life:
                        self.alert_window.time_clock(event)
                self.play_screen.timer(event)
                # 键盘按钮事件
                if event.type == KEYDOWN:
                    key_press = pygame.key.get_pressed()
                    # alt+f4退出
                    if key_press[K_LALT] and key_press[K_F4]:
                        pygame.display.quit()
                        exit()
                # 鼠标点击事件
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # 警告界面点击按钮
                    if self.alert_window:
                        if self.alert_window.life:
                            # 退出游戏
                            if self.alert_mod == 'exit':
                                if self.alert_window.button_click(pos) == '确定':
                                    self.alert_window = None
                                    pygame.display.quit()
                                    exit()
                                elif self.alert_window.button_click(pos) == '取消':
                                    self.alert_window = None
                            # 取消匹配
                            elif self.alert_mod == 'match':
                                if self.alert_window.button_click(pos) == '取消':
                                    self.alert_window = None
                                    self.play_screen.give_up_match()
                                    self.now_screen = 'menu'
                            # 保存配置成功,关于,游戏结束
                            elif self.alert_mod == 'save_success' or self.alert_mod == 'about' or self.alert_mod == 'result':
                                if self.alert_window.button_click(pos) == '确定':
                                    self.alert_window = None
                            # 提前退出游戏
                            elif self.alert_mod == 'end_game':
                                if self.alert_window.button_click(pos) == '确定':
                                    self.now_screen = 'menu'
                                    self.alert_window = None
                                elif self.alert_window.button_click(pos) == '取消':
                                    self.alert_window = None
                    # 菜单界面
                    elif self.now_screen == 'menu':
                        # 点击多人游戏
                        if self.menu_screen.button_play.isClicked(pos):
                            self.play_screen.__init__(self, self.screen)
                            self.now_screen = 'play'
                            self.alert_window = Window(self.screen, [self.screen.get_width()/2, self.screen.get_height()/2],
                                                       'alert1', 'loading', texts=['取消'])
                            self.alert_mod = 'match'
                            self.play_screen.go_match()
                        # 点击房间
                        if self.menu_screen.button_room.isClicked(pos):
                            self.now_screen = 'room'
                        # 点击记录
                        if self.menu_screen.button_record.isClicked(pos):
                            self.now_screen = 'record'
                        # 点击设置
                        if self.menu_screen.button_set.isClicked(pos):
                            self.now_screen = 'set'
                            self.set_screen.get_conf()
                        # 点击退出
                        if self.menu_screen.button_exit.isClicked(pos):
                            self.alert_window = Window(self.screen, [self.screen.get_width()/2, self.screen.get_height()/2],  'alert1', 'pause', texts=['确定', '取消'])
                            self.alert_mod = 'exit'
                        # 点击关于
                        if self.menu_screen.button_about.isClicked(pos):
                            self.alert_window = Window(self.screen, [self.screen.get_width()/2, self.screen.get_height()/2], 'alert2', '', texts=['确定'], rotate_speed=0)
                            self.alert_window.load_text('一个简陋的五子棋游戏', [self.screen.get_width()/2-150, self.screen.get_height()/2-100], text_info=['fangsong', 35, 0], col=[255, 0, 200])
                            self.alert_mod = 'about'
                    # 多人游戏界面
                    elif self.now_screen == 'play':
                        self.play_screen.mouse_click(pos)
                    # 房间界面
                    elif self.now_screen == 'room':
                        self.room_screen.mouse_click(pos)
                    # 记录界面
                    elif self.now_screen == 'record':
                        self.record_screen.mouse_click(pos)
                    # 设置界面
                    elif self.now_screen == 'set':
                        self.set_screen.mouse_click(pos)

            # ################## 画界面 ############################
            # 菜单界面
            if self.now_screen == 'menu':
                self.menu_screen.blit_button()
            # 游戏界面
            elif self.now_screen == 'play':
                self.play_screen.draw_stuff()
            # 房间界面
            elif self.now_screen == 'room':
                self.room_screen.draw_stuff()
            # 设置界面
            elif self.now_screen == 'set':
                self.set_screen.draw_stuff()
            # 记录界面
            elif self.now_screen == 'record':
                self.record_screen.draw_stuff()
            # 有警告界面
            if self.alert_window:
                if self.alert_window.life:
                    self.alert_window.draw_window()

            # ################## 画悬浮 ############################
            pos = pygame.mouse.get_pos()
            # 警告界面
            if self.alert_window:
                if self.alert_window.life:
                    self.alert_window.change_color(pos)
            # 菜单界面
            elif self.now_screen == 'menu':
                self.menu_screen.hover_button(pos)
            # 游戏界面
            elif self.now_screen == 'play':
                self.play_screen.mouse_hover(pos)
            # 房间界面
            elif self.now_screen == 'room':
                self.room_screen.mouse_hover(pos)
            # 设置界面
            elif self.now_screen == 'set':
                self.set_screen.mouse_hover(pos)
            # 设置界面
            elif self.now_screen == 'record':
                self.record_screen.mouse_hover(pos)
            # 刷新
            pygame.display.update()

#
# new_game = Game()
# new_game.began()
