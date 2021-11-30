import pygame
from 小工具.gametool.GameButton import Button
from 小工具.gametool.alert import Window
from requests import post


# 房间
class Room(object):
    def __init__(self, father, screen):
        self.father = father
        self.screen = screen
        # 按钮
        self.refresh_button = Button(self.screen, '刷新', [1200, 200], font_pos_alter=[40, 20])
        self.create_button = Button(self.screen, '创建房间', [1300, 200], font_pos_alter=[40, 20])
        self.back_button = Button(self.screen, '', [100, 100], mod='back', show_laplacian=2)

    # 所有房间
    def all_room(self):
        pass

    # 创建房间
    def create_room(self):
        json = {
            'num': self.father.user_num
        }
        response = post(self.father.server_ip+'create_room', json=json)

    def draw_stuff(self):
        self.back_button.drawButton()
        self.refresh_button.drawButton()

    def mouse_hover(self, pos):
        self.back_button.changeColor(pos)
        self.refresh_button.changeColor(pos)

    def mouse_click(self, pos):
        if self.back_button.isClicked(pos):
            self.father.now_screen = 'menu'
        elif self.refresh_button.isClicked(pos):
            pass
