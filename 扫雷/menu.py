import pygame
from gametool.GameButton import Button
from sys import exit
from gametool.alert import Window

pygame.init()


class Menu(object):
    def __init__(self, father):
        self.father = father
        # 按键
        self.easy = Button(self.father.screen, '低级', [self.father.size[0] // 2, self.father.size[1] // 3],
                           font_pos_alter=[30, 20])
        self.mid = Button(self.father.screen, '中级', [self.father.size[0] // 2, self.father.size[1] // 3 + 100],
                          font_pos_alter=[30, 20])
        self.hard = Button(self.father.screen, '高级', [self.father.size[0] // 2, self.father.size[1] // 3 + 200],
                           font_pos_alter=[30, 20])
        self.record = Button(self.father.screen, '数据', [self.father.size[0] // 2, self.father.size[1] // 3 + 300],
                             font_pos_alter=[30, 20])
        self.set = Button(self.father.screen, '设置', [self.father.size[0] // 2, self.father.size[1] // 3 + 400],
                          font_pos_alter=[30, 20])
        self.exit = Button(self.father.screen, '退出', [self.father.size[0] // 2, self.father.size[1] // 3 + 500],
                           font_pos_alter=[30, 20])
        self.about = Button(self.father.screen, '', [self.father.size[0] // 10, self.father.size[1] // 10],
                            mod='query', hover_pic='query_hover', font_pos_alter=[30, 20])
        self.button_list = [self.easy, self.mid, self.hard, self.record, self.set, self.exit, self.about]
        self.alert_window = None
        self.init()

    # 初始化
    def init(self):
        # 按键
        if self.father.size[0] == 1920:
            multiple = 1
            font_pos_alter = [30, 20]
        else:
            multiple = 0.7
            font_pos_alter = [20, 10]
        self.easy = Button(self.father.screen, '低级', [self.father.size[0] // 2, self.father.size[1] // 3],
                           multiple=multiple, font_pos_alter=font_pos_alter)
        self.mid = Button(self.father.screen, '中级', [self.father.size[0] // 2, self.father.size[1] // 3 + self.father.size[1]//10],
                          multiple=multiple, font_pos_alter=font_pos_alter)
        self.hard = Button(self.father.screen, '高级', [self.father.size[0] // 2, self.father.size[1] // 3 + self.father.size[1]//5],
                           multiple=multiple, font_pos_alter=font_pos_alter)
        self.record = Button(self.father.screen, '数据', [self.father.size[0] // 2, self.father.size[1] // 3 + self.father.size[1]//10*3],
                             multiple=multiple, font_pos_alter=font_pos_alter)
        self.set = Button(self.father.screen, '设置', [self.father.size[0] // 2, self.father.size[1] // 3 + self.father.size[1]//10*4],
                          multiple=multiple, font_pos_alter=font_pos_alter)
        self.exit = Button(self.father.screen, '退出', [self.father.size[0] // 2, self.father.size[1] // 3 + self.father.size[1]//2],
                           multiple=multiple, font_pos_alter=font_pos_alter)
        self.about = Button(self.father.screen, '', [self.father.size[0] // 10, self.father.size[1] // 10],
                            mod='query', hover_pic='query_hover', font_pos_alter=[30, 20], multiple=multiple)
        self.button_list = [self.easy, self.mid, self.hard, self.record, self.set, self.exit, self.about]
        self.alert_window = None

    def blit(self):
        for button in self.button_list:
            button.blit()
        if self.alert_window:
            self.alert_window.blit()

    def hover(self, pos):
        if self.alert_window:
            self.alert_window.hover(pos)
            return
        for button in self.button_list:
            button.hover(pos)

    def click(self, pos, btn):
        if btn == 0:
            if self.alert_window:
                if self.alert_window.click(pos):
                    self.alert_window = None
            elif self.easy.click(pos):
                self.father.game_screen.init()
                self.father.now_screen = self.father.game_screen
                self.father.game_screen.level = 'easy'
                self.father.game_screen.init()
            elif self.mid.click(pos):
                self.father.now_screen = self.father.game_screen
                self.father.game_screen.level = 'mid'
                self.father.game_screen.init()
            elif self.hard.click(pos):
                self.father.now_screen = self.father.game_screen
                self.father.game_screen.level = 'hard'
                self.father.game_screen.init()
            elif self.record.click(pos):
                self.father.now_screen = self.father.record_screen
                self.father.record_screen.init()
            elif self.set.click(pos):
                self.father.now_screen = self.father.set_screen
                self.father.set_screen.init()
            elif self.about.click(pos):
                self.alert_window = Window(self.father.screen, [self.father.size[0]//2, self.father.size[1]//2], window_mod='alert2', texts=['确定'], alert_mod='', rotate_speed=0)
                self.alert_window.load_text(['作者:yunyuyuan', '单击数字开周围块', '左ctrl调速'], [[self.father.size[0]//2-150, self.father.size[1]//2-100], [self.father.size[0]//2-150, self.father.size[1]//2-50], [self.father.size[0]//2-150, self.father.size[1]//2]], text_info=['fangsong', 30, 1])
            elif self.exit.click(pos):
                pygame.display.quit()
                exit()
