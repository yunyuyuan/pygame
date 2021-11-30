import pygame
from gametool.GameButton import Button
from json import dump

pygame.init()


class Set(object):
    def __init__(self, father):
        self.father = father
        self.back = Button(self.father.screen, '', [self.father.size[0]//20, self.father.size[1]//10], mod='back',
                           hover_pic='back_hover')
        self.save = Button(self.father.screen, '保存', [self.father.size[0]//2, self.father.size[1]-100],
                           font_pos_alter=[30, 20])
        self.set_1_source = pygame.image.load('images/pen.png').convert_alpha()
        self.set_2_source = pygame.image.load('images/pen.png').convert_alpha()
        self.set_3_source = pygame.image.load('images/pen.png').convert_alpha()
        self.set_4_source = pygame.image.load('images/pen.png').convert_alpha()
        self.set_1_source.blit(self.father.font.render('窗口', False, [255, 255, 255]), [95, 40])
        self.set_2_source.blit(self.father.font.render('背景', False, [255, 255, 255]), [95, 40])
        self.set_3_source.blit(self.father.font.render('样式', False, [255, 255, 255]), [95, 40])
        self.set_4_source.blit(self.father.font.render(' AI', False, [255, 255, 255]), [95, 40])
        self.size_1_source = pygame.image.load('images/size.png').convert_alpha()
        self.size_2_source = pygame.image.load('images/size.png').convert_alpha()
        self.size_1_source.blit(self.father.font.render('1920x1080', False, [255, 200, 10]), [5, 5])
        self.size_2_source.blit(self.father.font.render('1280x720', False, [255, 200, 100]), [5, 5])
        self.bg_1_source = pygame.transform.scale(self.father.bg_1, [192, 108])
        self.bg_2_source = pygame.transform.scale(self.father.bg_2, [192, 108])
        self.bg_3_source = pygame.transform.scale(self.father.bg_3, [192, 108])
        self.bg_4_source = pygame.transform.scale(self.father.bg_4, [192, 108])
        self.bg_5_source = pygame.transform.scale(self.father.bg_5, [192, 108])
        self.mine_1_source = pygame.image.load('images/mine1.png').convert_alpha()
        self.mine_2_source = pygame.image.load('images/mine2.png').convert_alpha()
        self.flag_1_source = pygame.image.load('images/flag1.png').convert_alpha()
        self.flag_2_source = pygame.image.load('images/flag2.png').convert_alpha()
        self.death_1_source = pygame.image.load('images/size.png').convert_alpha()
        self.death_2_source = pygame.image.load('images/size.png').convert_alpha()
        self.death_1_source.blit(self.father.font.render('不死猜', False, [150, 200, 100]), [5, 5])
        self.death_2_source.blit(self.father.font.render('死猜', False, [150, 200, 100]), [5, 5])
        self.mark_1_source = pygame.image.load('images/size.png').convert_alpha()
        self.mark_2_source = pygame.image.load('images/size.png').convert_alpha()
        self.mark_1_source.blit(self.father.font.render('不插旗', False, [150, 200, 100]), [5, 5])
        self.mark_2_source.blit(self.father.font.render('插旗', False, [150, 200, 100]), [5, 5])
        self.init()
        self.widget_list = [self.back, self.save]
        self.now_bg = self.father.now_bg
        self.now_size = self.father.size
        self.now_mine = self.father.now_mine
        self.now_flag = self.father.now_flag
        self.now_death = self.father.now_death
        self.now_mark = self.father.now_mark

    # 初始化
    def init(self):
        self.now_bg = self.father.now_bg
        self.now_size = self.father.size
        self.now_mine = self.father.now_mine
        self.now_flag = self.father.now_flag
        self.now_death = self.father.now_death
        self.now_mark = self.father.now_mark
        if self.father.size[0] == 1920:
            multiple = 1
            font_pos_alter = [30, 20]
            self.set_1_pos = [300, 100]
            self.set_2_pos = [300, 300]
            self.set_3_pos = [300, 500]
            self.set_4_pos = [300, 700]
            self.size_1_pos = [self.set_1_pos[0]+400, self.set_1_pos[1]+30]
            self.size_2_pos = [self.set_1_pos[0]+900, self.set_1_pos[1]+30]
            self.bg_1_pos = [600, self.set_2_pos[1]]
            self.bg_2_pos = [self.bg_1_pos[0]+250, self.bg_1_pos[1]]
            self.bg_3_pos = [self.bg_1_pos[0]+500, self.bg_1_pos[1]]
            self.bg_4_pos = [self.bg_1_pos[0]+750, self.bg_1_pos[1]]
            self.bg_5_pos = [self.bg_1_pos[0]+1000, self.bg_1_pos[1]]
            self.mine_1_pos = [self.set_3_pos[0]+350, self.set_3_pos[1]+25]
            self.mine_2_pos = [self.mine_1_pos[0]+150, self.mine_1_pos[1]]
            self.flag_1_pos = [self.mine_2_pos[0] + 280, self.set_3_pos[1]+25]
            self.flag_2_pos = [self.flag_1_pos[0] + 150, self.flag_1_pos[1]]
            self.death_1_pos = [self.set_4_pos[0] + 280, self.set_4_pos[1] + 25]
            self.death_2_pos = [self.death_1_pos[0] + 200, self.death_1_pos[1]]
            self.mark_1_pos = [self.death_2_pos[0] + 200, self.set_4_pos[1] + 25]
            self.mark_2_pos = [self.mark_1_pos[0] + 200, self.mark_1_pos[1]]
        else:
            multiple = 0.7
            font_pos_alter = [20, 10]
            self.set_1_pos = [130, 80]
            self.set_2_pos = [130, 220]
            self.set_3_pos = [130, 360]
            self.set_4_pos = [130, 500]
            self.size_1_pos = [self.set_1_pos[0] + 300, self.set_1_pos[1] + 20]
            self.size_2_pos = [self.set_1_pos[0] + 650, self.set_1_pos[1] + 20]
            self.bg_1_pos = [350, self.set_2_pos[1]]
            self.bg_2_pos = [self.bg_1_pos[0]+170, self.bg_1_pos[1]]
            self.bg_3_pos = [self.bg_1_pos[0]+340, self.bg_1_pos[1]]
            self.bg_4_pos = [self.bg_1_pos[0]+510, self.bg_1_pos[1]]
            self.bg_5_pos = [self.bg_1_pos[0]+680, self.bg_1_pos[1]]
            self.mine_1_pos = [self.set_3_pos[0] + 250, self.set_3_pos[1]+20]
            self.mine_2_pos = [self.mine_1_pos[0] + 100, self.mine_1_pos[1]]
            self.flag_1_pos = [self.mine_2_pos[0] + 200, self.set_3_pos[1]+20]
            self.flag_2_pos = [self.flag_1_pos[0] + 100, self.flag_1_pos[1]]
            self.death_1_pos = [self.set_4_pos[0] + 250, self.set_4_pos[1] + 20]
            self.death_2_pos = [self.death_1_pos[0] + 130, self.death_1_pos[1]]
            self.mark_1_pos = [self.death_2_pos[0] + 180, self.set_4_pos[1] + 20]
            self.mark_2_pos = [self.mark_1_pos[0] + 130, self.mark_1_pos[1]]
        self.back.__init__(self.father.screen, '', [self.father.size[0]//20, self.father.size[1]//10], mod='back',
                           multiple=multiple, hover_pic='back_hover')
        self.save.__init__(self.father.screen, '保存', [self.father.size[0]//2, self.father.size[1]*9//10],
                           multiple=multiple, font_pos_alter=font_pos_alter)
        # 几项设置
        self.set_1 = pygame.transform.scale(
                     self.set_1_source, [int(self.set_1_source.get_width()*multiple), int(self.set_1_source.get_height()*multiple)])
        self.set_2 = pygame.transform.scale(
                     self.set_2_source, [int(self.set_2_source.get_width()*multiple), int(self.set_2_source.get_height()*multiple)])
        self.set_3 = pygame.transform.scale(
                     self.set_3_source, [int(self.set_3_source.get_width() * multiple), int(self.set_3_source.get_height() * multiple)])
        self.set_4 = pygame.transform.scale(
                     self.set_4_source, [int(self.set_4_source.get_width() * multiple), int(self.set_4_source.get_height() * multiple)])
        # 大小
        self.size_1 = pygame.transform.scale(self.size_1_source, [int(200*multiple), int(50*multiple)])
        self.size_2 = pygame.transform.scale(self.size_2_source, [int(200*multiple), int(50*multiple)])
        self.bg_1 = pygame.transform.scale(self.bg_1_source, [int(192*multiple), int(108*multiple)])
        self.bg_2 = pygame.transform.scale(self.bg_2_source, [int(192*multiple), int(108*multiple)])
        self.bg_3 = pygame.transform.scale(self.bg_3_source, [int(192*multiple), int(108*multiple)])
        self.bg_4 = pygame.transform.scale(self.bg_4_source, [int(192*multiple), int(108*multiple)])
        self.bg_5 = pygame.transform.scale(self.bg_5_source, [int(192*multiple), int(108*multiple)])
        self.mine_1 = pygame.transform.scale(self.mine_1_source, [int(80*multiple), int(80*multiple)])
        self.mine_2 = pygame.transform.scale(self.mine_2_source, [int(80*multiple), int(80*multiple)])
        self.flag_1 = pygame.transform.scale(self.flag_1_source, [int(80 * multiple), int(80 * multiple)])
        self.flag_2 = pygame.transform.scale(self.flag_2_source, [int(80 * multiple), int(80 * multiple)])
        self.death_1 = pygame.transform.scale(self.death_1_source, [int(150 * multiple), int(50 * multiple)])
        self.death_2 = pygame.transform.scale(self.death_2_source, [int(150 * multiple), int(50 * multiple)])
        self.mark_1 = pygame.transform.scale(self.mark_1_source, [int(150 * multiple), int(50 * multiple)])
        self.mark_2 = pygame.transform.scale(self.mark_2_source, [int(150 * multiple), int(50 * multiple)])
        self.size_1_border = [self.size_1_pos[0], self.size_1_pos[0]+self.size_1.get_width(), self.size_1_pos[1], self.size_1_pos[1]+self.size_1.get_height()]
        self.size_2_border = [self.size_2_pos[0], self.size_2_pos[0]+self.size_2.get_width(), self.size_2_pos[1], self.size_2_pos[1]+self.size_1.get_height()]
        self.bg_1_border = [self.bg_1_pos[0], self.bg_1_pos[0]+self.bg_1.get_width(), self.bg_1_pos[1], self.bg_1_pos[1]+self.bg_1.get_height()]
        self.bg_2_border = [self.bg_2_pos[0], self.bg_2_pos[0]+self.bg_2.get_width(), self.bg_2_pos[1], self.bg_2_pos[1]+self.bg_2.get_height()]
        self.bg_3_border = [self.bg_3_pos[0], self.bg_3_pos[0]+self.bg_3.get_width(), self.bg_3_pos[1], self.bg_3_pos[1]+self.bg_3.get_height()]
        self.bg_4_border = [self.bg_4_pos[0], self.bg_4_pos[0]+self.bg_4.get_width(), self.bg_4_pos[1], self.bg_4_pos[1]+self.bg_4.get_height()]
        self.bg_5_border = [self.bg_5_pos[0], self.bg_5_pos[0]+self.bg_5.get_width(), self.bg_5_pos[1], self.bg_5_pos[1]+self.bg_5.get_height()]
        self.mine_1_border = [self.mine_1_pos[0], self.mine_1_pos[0] + self.mine_1.get_width(), self.mine_1_pos[1], self.mine_1_pos[1] + self.mine_1.get_height()]
        self.mine_2_border = [self.mine_2_pos[0], self.mine_2_pos[0] + self.mine_2.get_width(), self.mine_2_pos[1], self.mine_2_pos[1] + self.mine_2.get_height()]
        self.flag_1_border = [self.flag_1_pos[0], self.flag_1_pos[0] + self.flag_1.get_width(), self.flag_1_pos[1], self.flag_1_pos[1] + self.flag_1.get_height()]
        self.flag_2_border = [self.flag_2_pos[0], self.flag_2_pos[0] + self.flag_2.get_width(), self.flag_2_pos[1], self.flag_2_pos[1] + self.flag_2.get_height()]
        self.death_1_border = [self.death_1_pos[0], self.death_1_pos[0] + self.death_1.get_width(), self.death_1_pos[1], self.death_1_pos[1] + self.death_1.get_height()]
        self.death_2_border = [self.death_2_pos[0], self.death_2_pos[0] + self.death_2.get_width(), self.death_2_pos[1], self.death_2_pos[1] + self.death_2.get_height()]
        self.mark_1_border = [self.mark_1_pos[0], self.mark_1_pos[0] + self.mark_1.get_width(), self.mark_1_pos[1], self.mark_1_pos[1] + self.mark_1.get_height()]
        self.mark_2_border = [self.mark_2_pos[0], self.mark_2_pos[0] + self.mark_2.get_width(), self.mark_2_pos[1], self.mark_2_pos[1] + self.mark_2.get_height()]

    def blit(self):
        for widget in self.widget_list:
            widget.blit()
        self.father.screen.blit(self.set_1, self.set_1_pos)
        self.father.screen.blit(self.set_2, self.set_2_pos)
        self.father.screen.blit(self.set_3, self.set_3_pos)
        self.father.screen.blit(self.set_4, self.set_4_pos)
        self.father.screen.blit(self.size_1, self.size_1_pos)
        self.father.screen.blit(self.size_2, self.size_2_pos)
        self.father.screen.blit(self.bg_1, self.bg_1_pos)
        self.father.screen.blit(self.bg_2, self.bg_2_pos)
        self.father.screen.blit(self.bg_3, self.bg_3_pos)
        self.father.screen.blit(self.bg_4, self.bg_4_pos)
        self.father.screen.blit(self.bg_5, self.bg_5_pos)
        self.father.screen.blit(self.mine_1, self.mine_1_pos)
        self.father.screen.blit(self.mine_2, self.mine_2_pos)
        self.father.screen.blit(self.flag_1, self.flag_1_pos)
        self.father.screen.blit(self.flag_2, self.flag_2_pos)
        self.father.screen.blit(self.death_1, self.death_1_pos)
        self.father.screen.blit(self.death_2, self.death_2_pos)
        self.father.screen.blit(self.mark_1, self.mark_1_pos)
        self.father.screen.blit(self.mark_2, self.mark_2_pos)
        if self.now_size[0] == 1920:
            pygame.draw.rect(self.father.screen, [0, 0, 0], [self.size_1_border[0], self.size_1_border[2],
                                                             self.size_1_border[1] - self.size_1_border[0],
                                                             self.size_1_border[3] - self.size_1_border[2]], 2)
        else:
            pygame.draw.rect(self.father.screen, [0, 0, 0], [self.size_2_border[0], self.size_2_border[2],
                                                             self.size_2_border[1] - self.size_2_border[0],
                                                             self.size_2_border[3] - self.size_2_border[2]], 2)
        exec("pygame.draw.rect(self.father.screen, [0, 0, 0], [self.bg_{0}_border[0], self.bg_{0}_border[2],"
             "self.bg_{0}_border[1] - self.bg_{0}_border[0],self.bg_{0}_border[3] - self.bg_{0}_border[2]], 2)".format(self.now_bg+1))
        exec("pygame.draw.rect(self.father.screen, [0, 0, 0], [self.mine_{0}_border[0], self.mine_{0}_border[2],"
             "self.mine_{0}_border[1] - self.mine_{0}_border[0],self.mine_{0}_border[3] - self.mine_{0}_border[2]], 2)".format(
            self.now_mine + 1))
        exec("pygame.draw.rect(self.father.screen, [0, 0, 0], [self.flag_{0}_border[0], self.flag_{0}_border[2],"
             "self.flag_{0}_border[1] - self.flag_{0}_border[0],self.flag_{0}_border[3] - self.flag_{0}_border[2]], 2)".format(
            self.now_flag + 1))
        exec("pygame.draw.rect(self.father.screen, [0, 0, 0], [self.death_{0}_border[0], self.death_{0}_border[2],"
             "self.death_{0}_border[1] - self.death_{0}_border[0],self.death_{0}_border[3] - self.death_{0}_border[2]], 2)".format(
            self.now_death + 1))
        exec("pygame.draw.rect(self.father.screen, [0, 0, 0], [self.mark_{0}_border[0], self.mark_{0}_border[2],"
             "self.mark_{0}_border[1] - self.mark_{0}_border[0],self.mark_{0}_border[3] - self.mark_{0}_border[2]], 2)".format(
            self.now_mark + 1))

    def hover(self, pos):
        for widget in self.widget_list:
            widget.hover(pos)
        if self.size_1_border[0] <= pos[0] <= self.size_1_border[1] and self.size_1_border[2] <= pos[1] <= self.size_1_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.size_1_border[0], self.size_1_border[2],
                             self.size_1_border[1]-self.size_1_border[0], self.size_1_border[3]-self.size_1_border[2]], 2)
        elif self.size_2_border[0] <= pos[0] <= self.size_2_border[1] and self.size_2_border[2] <= pos[1] <= self.size_2_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.size_2_border[0], self.size_2_border[2],
                             self.size_2_border[1]-self.size_2_border[0], self.size_2_border[3]-self.size_2_border[2]], 2)
        elif self.bg_1_border[0] <= pos[0] <= self.bg_1_border[1] and self.bg_1_border[2] <= pos[1] <= self.bg_1_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.bg_1_border[0], self.bg_1_border[2],
                             self.bg_1_border[1]-self.bg_1_border[0], self.bg_1_border[3]-self.bg_1_border[2]], 2)
        elif self.bg_2_border[0] <= pos[0] <= self.bg_2_border[1] and self.bg_2_border[2] <= pos[1] <= self.bg_2_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.bg_2_border[0], self.bg_2_border[2],
                             self.bg_2_border[1]-self.bg_2_border[0], self.bg_2_border[3]-self.bg_2_border[2]], 2)
        elif self.bg_3_border[0] <= pos[0] <= self.bg_3_border[1] and self.bg_3_border[2] <= pos[1] <= self.bg_3_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.bg_3_border[0], self.bg_3_border[2],
                             self.bg_3_border[1]-self.bg_3_border[0], self.bg_3_border[3]-self.bg_3_border[2]], 2)
        elif self.bg_4_border[0] <= pos[0] <= self.bg_4_border[1] and self.bg_4_border[2] <= pos[1] <= self.bg_4_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.bg_4_border[0], self.bg_4_border[2],
                             self.bg_4_border[1]-self.bg_4_border[0], self.bg_4_border[3]-self.bg_4_border[2]], 2)
        elif self.bg_5_border[0] <= pos[0] <= self.bg_5_border[1] and self.bg_5_border[2] <= pos[1] <= self.bg_5_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.bg_5_border[0], self.bg_5_border[2],
                             self.bg_5_border[1]-self.bg_5_border[0], self.bg_5_border[3]-self.bg_5_border[2]], 2)
        elif self.mine_1_border[0] <= pos[0] <= self.mine_1_border[1] and self.mine_1_border[2] <= pos[1] <= self.mine_1_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.mine_1_border[0], self.mine_1_border[2],
                             self.mine_1_border[1]-self.mine_1_border[0], self.mine_1_border[3]-self.mine_1_border[2]], 2)
        elif self.mine_2_border[0] <= pos[0] <= self.mine_2_border[1] and self.mine_2_border[2] <= pos[1] <= self.mine_2_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.mine_2_border[0], self.mine_2_border[2],
                             self.mine_2_border[1]-self.mine_2_border[0], self.mine_2_border[3]-self.mine_2_border[2]], 2)
        elif self.flag_1_border[0] <= pos[0] <= self.flag_1_border[1] and self.flag_1_border[2] <= pos[1] <= self.flag_1_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.flag_1_border[0], self.flag_1_border[2],
                             self.flag_1_border[1]-self.flag_1_border[0], self.flag_1_border[3]-self.flag_1_border[2]], 2)
        elif self.flag_2_border[0] <= pos[0] <= self.flag_2_border[1] and self.flag_2_border[2] <= pos[1] <= self.flag_2_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.flag_2_border[0], self.flag_2_border[2],
                             self.flag_2_border[1]-self.flag_2_border[0], self.flag_2_border[3]-self.flag_2_border[2]], 2)
        elif self.death_1_border[0] <= pos[0] <= self.death_1_border[1] and self.death_1_border[2] <= pos[1] <= self.death_1_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.death_1_border[0], self.death_1_border[2],
                             self.death_1_border[1]-self.death_1_border[0], self.death_1_border[3]-self.death_1_border[2]], 2)
        elif self.death_2_border[0] <= pos[0] <= self.death_2_border[1] and self.death_2_border[2] <= pos[1] <= self.death_2_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.death_2_border[0], self.death_2_border[2],
                             self.death_2_border[1]-self.death_2_border[0], self.death_2_border[3]-self.death_2_border[2]], 2)
        elif self.mark_1_border[0] <= pos[0] <= self.mark_1_border[1] and self.mark_1_border[2] <= pos[1] <= self.mark_1_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.mark_1_border[0], self.mark_1_border[2],
                             self.mark_1_border[1]-self.mark_1_border[0], self.mark_1_border[3]-self.mark_1_border[2]], 2)
        elif self.mark_2_border[0] <= pos[0] <= self.mark_2_border[1] and self.mark_2_border[2] <= pos[1] <= self.mark_2_border[3]:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.mark_2_border[0], self.mark_2_border[2],
                             self.mark_2_border[1]-self.mark_2_border[0], self.mark_2_border[3]-self.mark_2_border[2]], 2)

    def click(self, pos, btn):
        if btn == 0:
            if self.back.click(pos):
                self.father.now_screen = self.father.menu_screen
            elif self.size_1_border[0] <= pos[0] <= self.size_1_border[1] and self.size_1_border[2] <= pos[1] <= self.size_1_border[3]:
                self.now_size = [1920, 1080]
            elif self.size_2_border[0] <= pos[0] <= self.size_2_border[1] and self.size_2_border[2] <= pos[1] <= self.size_2_border[3]:
                self.now_size = [1280, 720]
            elif self.bg_1_border[0] <= pos[0] <= self.bg_1_border[1] and self.bg_1_border[2] <= pos[1] <= self.bg_1_border[3]:
                self.now_bg = 0
            elif self.bg_2_border[0] <= pos[0] <= self.bg_2_border[1] and self.bg_2_border[2] <= pos[1] <= self.bg_2_border[3]:
                self.now_bg = 1
            elif self.bg_3_border[0] <= pos[0] <= self.bg_3_border[1] and self.bg_3_border[2] <= pos[1] <= self.bg_3_border[3]:
                self.now_bg = 2
            elif self.bg_4_border[0] <= pos[0] <= self.bg_4_border[1] and self.bg_4_border[2] <= pos[1] <= self.bg_4_border[3]:
                self.now_bg = 3
            elif self.bg_5_border[0] <= pos[0] <= self.bg_5_border[1] and self.bg_5_border[2] <= pos[1] <= self.bg_5_border[3]:
                self.now_bg = 4
            elif self.mine_1_border[0] <= pos[0] <= self.mine_1_border[1] and self.mine_1_border[2] <= pos[1] <= self.mine_1_border[3]:
                self.now_mine = 0
            elif self.mine_2_border[0] <= pos[0] <= self.mine_2_border[1] and self.mine_2_border[2] <= pos[1] <= self.mine_2_border[3]:
                self.now_mine = 1
            elif self.flag_1_border[0] <= pos[0] <= self.flag_1_border[1] and self.flag_1_border[2] <= pos[1] <= self.flag_1_border[3]:
                self.now_flag = 0
            elif self.flag_2_border[0] <= pos[0] <= self.flag_2_border[1] and self.flag_2_border[2] <= pos[1] <= self.flag_2_border[3]:
                self.now_flag = 1
            elif self.death_1_border[0] <= pos[0] <= self.death_1_border[1] and self.death_1_border[2] <= pos[1] <= self.death_1_border[3]:
                self.now_death = 0
            elif self.death_2_border[0] <= pos[0] <= self.death_2_border[1] and self.death_2_border[2] <= pos[1] <= self.death_2_border[3]:
                self.now_death = 1
            elif self.mark_1_border[0] <= pos[0] <= self.mark_1_border[1] and self.mark_1_border[2] <= pos[1] <= self.mark_1_border[3]:
                self.now_mark = 0
            elif self.mark_2_border[0] <= pos[0] <= self.mark_2_border[1] and self.mark_2_border[2] <= pos[1] <= self.mark_2_border[3]:
                self.now_mark = 1
            elif self.save.click(pos):
                # 保存配置
                mod = 0
                if self.now_size[0] == 1920:
                    mod = -2147483648
                dump([self.now_size, mod, self.now_bg, self.now_mine, self.now_flag, self.now_death, self.now_mark], open('config.json', 'w'))
                # 重新加载
                if self.now_size != self.father.size:
                    self.father.init(update=True)
                else:
                    self.father.init()
                self.father.now_screen = self.father.set_screen
