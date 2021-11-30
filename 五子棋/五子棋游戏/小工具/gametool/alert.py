import pygame
from pygame.locals import *
try:
    from .GameButton import Button
except:
    from GameButton import Button
pygame.init()


# 创造一个提示窗口
class Window(object):
    def __init__(self, surface, pos, window_mod, alert_mod, texts=['确定', '取消'], rotate_speed=10, text_info=['', [0, 0], ['kaiti', 20, 0]]):
        """

        :param surface: 绘制的surface
        :param pos: 绘制的坐标
        :param text: 提醒文字，为''不绘制
        :param window_mod: 窗口的样式
        :param alert_mod: 提示的样式
        :param texts: 几个的文字按钮
        """
        self.screen = surface
        self.text = None
        self.text_pos = None
        self.texts = texts
        # 窗口背景
        self.window = pygame.image.load('./小工具/gametool/' + window_mod + '.png').convert_alpha()
        self.window_width = self.window.get_width()
        self.window_height = self.window.get_height()
        # 警告图标
        self.load_alert(alert_mod, rotate_speed)
        # 警告文字
        self.load_text(*text_info)
        # 窗口位置
        self.pos = [pos[0] - self.window_width//2, pos[1] - self.window_height//2]
        # 几个按钮
        for i in range(len(self.texts)):
            exec('self.button%d = Button(self.screen, self.texts[i], [surface.get_width()/2-self.window_width//2+(self.window_width*(i+1)/%d), surface.get_height()/2-self.window_height//2+self.window_height-100], multiple=0.7, font_pos_alter=[30, 20])' % (i+1, len(self.texts)+1))
        # 是否还存在
        self.life = True

    # 计时事件
    def time_clock(self, event):
        if self.rotate_speed != 0 and event.type == self.count:
            self.rotate_angle += 1

    # 添加/删除警告
    def load_alert(self, alert_mod, rotate_speed):
        if alert_mod != '':
            self.alert = pygame.image.load('./小工具/gametool/' + alert_mod + '.png').convert_alpha()
            self.alert_width = self.alert.get_width()
            self.alert_height = self.alert.get_height()
        else:
            self.alert = None
        # 计时器
        self.rotate_speed = rotate_speed
        if self.rotate_speed != 0:
            self.count = pygame.USEREVENT + 1
            pygame.time.set_timer(self.count, rotate_speed)
            # 旋转角度
            self.rotate_angle = 0
        
    # 添加/删除文字
    def load_text(self, text, pos, text_info=['kaiti', 30, 0], col=[0, 0, 0]):
        if text != '':
            self.text = pygame.font.SysFont(*text_info).render(text, 0, col)
            self.text_pos = pos
        else:
            self.text = None
    
    # 画出窗口和按钮
    def draw_window(self):
        self.screen.blit(self.window, self.pos)
        if self.rotate_speed != 0:
            if self.rotate_angle == 360:
                self.rotate_angle = 0
            new_alert = pygame.transform.rotate(self.alert, self.rotate_angle)
        else:
            new_alert = self.alert
        if self.alert:
            self.screen.blit(new_alert, [self.pos[0]+(self.window_width//2)-new_alert.get_width()/2, self.pos[1]+(self.window_height//2)-new_alert.get_height()/2])
        # 画出文字
        if self.text:
            self.screen.blit(self.text, self.text_pos)
        # 画出按钮
        for i in range(len(self.texts)):
            exec('self.button%d.drawButton()' % (i+1))

    # 鼠标在按钮上悬浮
    def change_color(self, pos):
        for i in range(len(self.texts)):
            exec('self.button%d.changeColor(pos)' % (i+1))

    # 鼠标点击
    def button_click(self, pos):
        for i in range(len(self.texts)):
            is_click = eval('self.button%d.isClicked(pos)' % (i+1))
            if is_click:
                # 完成，退出
                self.life = False
                return self.texts[i]
