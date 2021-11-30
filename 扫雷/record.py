import pygame
from gametool.GameButton import Button
from json import load

pygame.init()


class Record(object):
    def __init__(self, father):
        self.father = father
        self.font = pygame.font.SysFont('fangsong', 40, True)
        self.lvl_1_source = pygame.image.load('images/pen.png').convert_alpha()
        self.lvl_2_source = pygame.image.load('images/pen.png').convert_alpha()
        self.lvl_3_source = pygame.image.load('images/pen.png').convert_alpha()
        self.lvl_1_source.blit(self.font.render('低级', False, [255, 255, 255]), [90, 40])
        self.lvl_2_source.blit(self.font.render('中级', False, [255, 255, 255]), [90, 40])
        self.lvl_3_source.blit(self.font.render('高级', False, [255, 255, 255]), [90, 40])
        self.back = Button(self.father.screen, '', [self.father.size[0] // 20, self.father.size[1] // 10], mod='back',
                           hover_pic='back_hover')
        self.init()

    # 初始化
    def init(self):
        self.info_1 = pygame.image.load('images/line.png').convert_alpha()
        self.info_2 = pygame.image.load('images/line.png').convert_alpha()
        self.info_3 = pygame.image.load('images/line.png').convert_alpha()
        # 读取记录
        info = load(open('record.json', 'r'))
        if self.father.size[0] == 1920:
            multiple = 1
            self.lvl_1_pos = [570, 200]
            self.lvl_2_pos = [self.lvl_1_pos[0]+260, self.lvl_1_pos[1]]
            self.lvl_3_pos = [self.lvl_1_pos[0]+520, self.lvl_1_pos[1]]
            self.info_1_pos = [300, 400]
            self.info_2_pos = [self.info_1_pos[0], self.info_1_pos[1]+200]
            self.info_3_pos = [self.info_1_pos[0], self.info_1_pos[1]+400]
        else:
            multiple = 0.7
            self.lvl_1_pos = [400, 100]
            self.lvl_2_pos = [self.lvl_1_pos[0] + 180, self.lvl_1_pos[1]]
            self.lvl_3_pos = [self.lvl_1_pos[0] + 360, self.lvl_1_pos[1]]
            self.info_1_pos = [200, 200]
            self.info_2_pos = [self.info_1_pos[0], self.info_1_pos[1] + 150]
            self.info_3_pos = [self.info_1_pos[0], self.info_1_pos[1] + 300]
        font = pygame.font.SysFont('kaiti', 100, False)
        self.info_1 = pygame.image.load('images/line.png').convert_alpha()
        self.info_2 = pygame.image.load('images/line.png').convert_alpha()
        self.info_3 = pygame.image.load('images/line.png').convert_alpha()
        self.info_1.blit(font.render('最佳时间', False, [255, 0, 255]), [50, 100])
        self.info_1.blit(font.render(str(info[0][0]), False, [255, 0, 255]), [600, 100])
        self.info_1.blit(font.render(str(info[1][0]), False, [255, 0, 255]), [1100, 100])
        self.info_1.blit(font.render(str(info[2][0]), False, [255, 0, 255]), [1600, 100])
        self.info_2.blit(font.render('总局数', False, [255, 255, 0]), [50, 100])
        self.info_2.blit(font.render(str(info[0][1]), False, [255, 255, 0]), [600, 100])
        self.info_2.blit(font.render(str(info[1][1]), False, [255, 255, 0]), [1100, 100])
        self.info_2.blit(font.render(str(info[2][1]), False, [255, 255, 0]), [1600, 100])
        self.info_3.blit(font.render('获胜局数', False, [0, 255, 255]), [50, 100])
        self.info_3.blit(font.render(str(info[0][2]), False, [0, 255, 255]), [600, 100])
        self.info_3.blit(font.render(str(info[1][2]), False, [0, 255, 255]), [1100, 100])
        self.info_3.blit(font.render(str(info[2][2]), False, [0, 255, 255]), [1600, 100])

        self.lvl_1 = pygame.transform.scale(self.lvl_1_source, [int(200*multiple), int(100*multiple)])
        self.lvl_2 = pygame.transform.scale(self.lvl_2_source, [int(200*multiple), int(100*multiple)])
        self.lvl_3 = pygame.transform.scale(self.lvl_3_source, [int(200*multiple), int(100*multiple)])
        self.info_1 = pygame.transform.scale(self.info_1, [int(1100*multiple), int(130*multiple)])
        self.info_2 = pygame.transform.scale(self.info_2, [int(1100*multiple), int(130*multiple)])
        self.info_3 = pygame.transform.scale(self.info_3, [int(1100*multiple), int(130*multiple)])
        self.back = Button(self.father.screen, '', [self.father.size[0] // 20, self.father.size[1] // 10], mod='back',
                           hover_pic='back_hover')

    def blit(self):
        self.back.blit()
        self.father.screen.blit(self.lvl_1, self.lvl_1_pos)
        self.father.screen.blit(self.lvl_2, self.lvl_2_pos)
        self.father.screen.blit(self.lvl_3, self.lvl_3_pos)
        self.father.screen.blit(self.info_1, self.info_1_pos)
        self.father.screen.blit(self.info_2, self.info_2_pos)
        self.father.screen.blit(self.info_3, self.info_3_pos)

    def hover(self, pos):
        self.back.hover(pos)

    def click(self, pos, btn):
        if btn == 0:
            if self.back.click(pos):
                self.father.now_screen = self.father.menu_screen
