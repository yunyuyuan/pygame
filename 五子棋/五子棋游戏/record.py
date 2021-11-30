import pygame
from 小工具.gametool.GameButton import Button


# 房间
class Record(object):
    def __init__(self, father, screen):
        self.father = father
        self.screen = screen
        # 按钮
        self.back_button = Button(self.screen, '', [100, 100], mod='back', show_laplacian=2)

    def draw_stuff(self):
        self.back_button.drawButton()

    def mouse_hover(self, pos):
        self.back_button.changeColor(pos)

    def mouse_click(self, pos):
        if self.back_button.isClicked(pos):
            self.father.now_screen = 'menu'

