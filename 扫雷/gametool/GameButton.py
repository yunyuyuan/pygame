import pygame
pygame.init()


# 矩形按钮
class Button(object):
    def __init__(self, surface, text, pos, multiple=1, font_info=['kaiti', 35, 0], font_pos_alter=[0, 0], col=[0, 0, 0], change_color=[255, 0, 0], mod='button1', show_laplacian=0, hover_pic=None):
        """

        :param surface: 要绘画的surface
        :param text: 按钮上的文字，可以设置为''
        :param pos: 按钮安放的坐标(中心)
        :param multiple: 按钮缩放的倍数，默认1倍
        :param font_info: 按钮文字的[字体，大小，是否加粗]
        :param font_pos_alter: 文字位置的底数，会随着按钮大小而偏差，酌情改变
        :param col: 按钮上文字的颜色，默认黑色
        :param change_color: 鼠标放在按钮上时按钮上文字的颜色，默认红色
        :param mod: 按钮的模型，默认button1
        :param show_laplacian: 设置鼠标放上去时是否显示按钮轮廓，1为矩形，2为圆形， 默认否
        :param hover_pic: 是否有Hover的图片
        """
        self.surface = surface
        self.pos = pos
        self.text = text
        self.font_under = font_pos_alter
        self.font = pygame.font.SysFont(font_info[0], int(font_info[1]*multiple), font_info[2])
        self.color = col
        self.change_color = change_color
        self.show_laplacian = show_laplacian
        self.has_hover_pic = False
        self.hover_pic = None
        if hover_pic:
            self.has_hover_pic = True
            self.hover_pic = pygame.image.load('gametool/' + hover_pic+'.png').convert_alpha()

        self.button = pygame.image.load('gametool/' + mod+'.png').convert_alpha()
        # 对按钮缩放
        self.button = pygame.transform.scale(self.button, (int(self.button.get_width()*multiple),
                                                           int(self.button.get_height()*multiple)))
        if hover_pic:
            self.hover_pic = pygame.transform.scale(self.hover_pic, (int(self.hover_pic.get_width() * multiple),
                                                                     int(self.hover_pic.get_height() * multiple)))
        # 计算按钮左上角位置和文字位置
        self.button_pos = [self.pos[0] - self.button.get_width()//2, self.pos[1] - self.button.get_height()//2]
        self.font_pos = [self.pos[0] - self.font_under[0],
                         self.pos[1] - self.font_under[1]]

    # 画出按钮
    def blit(self):
        """ blit方法画出按钮，文字 -> return None """
        self.surface.blit(self.button, self.button_pos)
        # 画出非空的文字
        if self.text != '':
            text = self.font.render(str(self.text), True, self.color)
            self.surface.blit(text, self.font_pos)

    # 动态改变颜色
    def hover(self, pos):
        """ blit方法画出轮廓，文字 -> return None """
        # 有Hover的图片
        if self.has_hover_pic:
            if self.button_pos[0] <= pos[0] <= self.button_pos[0] + self.button.get_width() and \
                    self.button_pos[1] <= pos[1] <= self.button_pos[1] + self.button.get_height():
                self.surface.blit(self.hover_pic, self.button_pos)
        # 画出圆形边框
        elif self.show_laplacian == 2:
            if ((pos[0] - self.pos[0]) ** 2 + (pos[1] - self.pos[1]) ** 2) ** 0.5 <= self.button.get_width() // 2:
                # 非空文字
                text = self.font.render(str(self.text), True, self.change_color)
                self.surface.blit(text, self.font_pos)
                # 圆形边框
                pygame.draw.circle(self.surface, self.change_color, self.pos, self.button.get_width()//2 + 5, 3)
        # 画出矩形边框
        else:
            if self.button_pos[0] <= pos[0] <= self.button_pos[0] + self.button.get_width() and \
                    self.button_pos[1] <= pos[1] <= self.button_pos[
                    1] + self.button.get_height():
                if self.text != '':
                    # 非空文字
                    text = self.font.render(str(self.text), True, self.change_color)
                    self.surface.blit(text, self.font_pos)
                # 矩形框
                pygame.draw.rect(self.surface, self.change_color,
                                 [*self.button_pos, self.button.get_width(), self.button.get_height()], 2)

    # 判断点击
    def click(self, pos):
        """ 判断pos是否在按钮内 -> return None """
        # 圆形
        if self.show_laplacian == 2:
            if ((pos[0] - self.pos[0])**2 + (pos[1] - self.pos[1])**2)**0.5 <= self.button.get_width()//2:
                return True
            else:
                return False
        else:
            if self.button_pos[0] <= pos[0] <= self.button_pos[0] + self.button.get_width() and \
                    self.button_pos[1] <= pos[1] <= self.button_pos[1] + self.button.get_height():
                return True
            else:
                return False

