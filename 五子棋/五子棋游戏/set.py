import pygame
from 小工具.gametool.GameButton import Button
from 小工具.gametool.alert import Window
from requests import post
from json import loads


# 设置界面
class Set(object):
    def __init__(self, father, surface):
        self.screen = surface
        self.father = father
        self.font = pygame.font.SysFont('fangsong', 35)
        self.all_bg = ['default', 'illusory', 'night', 'wood']
        self.all_avatar = ['mouse', 'cow', 'tiger', 'rabbit', 'dragon', 'snake', 'horse', 'sheep', 'monkey', 'chicken', 'dog', 'pig']
        self.choose = pygame.image.load('./images/choose.png').convert_alpha()
        # 选择的棋子
        self.choose_man = 'white'
        self.choose_bg = 'default'
        self.choose_avatar = 'mouse'
        self.name = None
        # 背景,头像
        self.bg_pic = pygame.image.load('./images/checkerboard_bg/illusory.jpg').convert()
        self.avatar_pic = pygame.image.load('./images/user_avatar/mouse.png').convert()
        self.get_conf()
        # 初始化背景
        for im in self.all_bg:
            exec("self.%s = pygame.transform.scale(pygame.image.load('./images/checkerboard_bg/%s.jpg').convert(), [200, 200])" % (im, im))
        # 初始化头像
        for im in self.all_avatar:
            exec("self.%s = pygame.transform.scale(pygame.image.load('./images/user_avatar/%s.png').convert(), [80, 80])" % (im, im))
        # 返回按钮
        self.back = Button(self.screen, '', [100, 100], mod='back', show_laplacian=2)
        # 保存按钮
        self.save = Button(self.screen, '保存', [self.screen.get_width()/2, self.screen.get_height()-100], font_pos_alter=[35, 20])

    # 请求配置
    def get_conf(self):
        json = {
            'num': self.father.user_num
        }
        data = post(self.father.server_ip+'get_conf', json=json)
        data = loads(data.content.decode('utf-8'))
        self.name = data[0]
        [self.choose_man, self.choose_bg, self.choose_avatar] = eval(data[1])
        if self.choose_bg == 'default':
            self.bg_pic = None
        else:
            self.bg_pic = pygame.image.load('./images/checkerboard_bg/%s.jpg' % self.choose_bg).convert()
        self.avatar_pic = pygame.transform.scale(pygame.image.load('./images/user_avatar/%s.png' % self.choose_avatar).convert(), [100, 100])

    # 上传配置
    def set_conf(self):
        json = {
            'num': self.father.user_num,
            'man': self.choose_man,
            'bg': self.choose_bg,
            'avatar': self.choose_avatar,
        }
        post(self.father.server_ip + 'set_conf', json=json)
        if self.choose_bg == 'default':
            self.bg_pic = None
        else:
            self.bg_pic = pygame.image.load('./images/checkerboard_bg/%s.jpg' % self.choose_bg).convert()
        self.avatar_pic = pygame.transform.scale(pygame.image.load('./images/user_avatar/%s.png' % self.choose_avatar).convert(), [100, 100])

        self.father.alert_window = Window(self.screen, [self.screen.get_width()/2, self.screen.get_height()/2], 'alert1', 'success', rotate_speed=0, texts=['确定'])
        self.father.alert_mod = 'save_success'

    # 画固件
    def draw_stuff(self):
        # 返回按钮
        self.back.drawButton()
        # 黑白棋子
        self.screen.blit(self.father.play_screen.white_man, [self.screen.get_width()/2-100-self.father.play_screen.man_width, 100])
        self.screen.blit(self.father.play_screen.black_man, [self.screen.get_width()/2+100, 100])
        # 背景
        for i in range(len(self.all_bg)):
            exec('self.screen.blit(self.%s, [%d, 200])' % (self.all_bg[i], self.screen.get_width()/2 - 550 + i*300))
        # 头像
        for i in range(len(self.all_avatar)):
            exec('self.screen.blit(self.%s, [%d, %d])' % (self.all_avatar[i], self.screen.get_width()/2 - 280 + (i % 4)*160, (i//4)*150+500))
        self.screen.blit(self.font.render('棋子偏好', 1, [0, 0, 0]), [600, 110])
        self.screen.blit(self.font.render('棋盘背景', 1, [0, 0, 0]), [150, 280])
        self.screen.blit(self.font.render('头像', 1, [0, 0, 0]), [450, 680])
        # 选择的棋子
        if self.choose_man == 'white':
            self.screen.blit(self.choose, [self.screen.get_width()/2-100-self.father.play_screen.man_width/2-self.choose.get_width()/2, 100+self.father.play_screen.man_height/2-self.choose.get_height()/2])
        else:
            self.screen.blit(self.choose, [self.screen.get_width()/2+100+self.father.play_screen.man_width/2-self.choose.get_width()/2, 100+self.father.play_screen.man_height/2-self.choose.get_height()/2])
        # 选择的背景
        self.screen.blit(self.choose, [self.screen.get_width()/2 - 400 + self.all_bg.index(self.choose_bg)*300-self.choose.get_width()/2, 350-self.choose.get_height()/2])
        # 选择的头像
        self.screen.blit(self.choose, [self.screen.get_width()/2 - 250 + (self.all_avatar.index(self.choose_avatar) % 4)*160, 535 + (self.all_avatar.index(self.choose_avatar) // 4)*150])
        # 保存按钮
        self.save.drawButton()

    # 鼠标悬浮
    def mouse_hover(self, pos):
        # 返回按钮
        self.back.changeColor(pos)
        # 放在棋子上
        if 100 <= pos[1] <= 100+self.father.play_screen.man_height:
            if self.screen.get_width()/2-100-self.father.play_screen.man_width <= pos[0] <= self.screen.get_width()/2-100 and self.choose_man == 'black':
                pygame.draw.rect(self.screen, [255, 0, 255], [self.screen.get_width()/2-100-self.father.play_screen.man_width, 100, self.father.play_screen.man_width, self.father.play_screen.man_height], 2)
            elif self.screen.get_width()/2+100 <= pos[0] <= self.screen.get_width()/2+100+self.father.play_screen.man_width and self.choose_man == 'white':
                pygame.draw.rect(self.screen, [255, 0, 255], [self.screen.get_width()/2+100, 100, self.father.play_screen.man_width, self.father.play_screen.man_height], 2)
        # 放在背景上
        elif 200 <= pos[1] <= 400:
            for i in range(len(self.all_bg)):
                if self.screen.get_width()/2 - 550 + i*300 <= pos[0] <= self.screen.get_width()/2 - 350 + i*300:
                    pygame.draw.rect(self.screen, [255, 0, 255], [self.screen.get_width()/2 - 550 + i*300, 200, 200, 200], 2)
                    break
        # 放在头像上
        for i in range(len(self.all_avatar)):
            if self.screen.get_width()/2 - 280 + (i % 4)*160 <= pos[0] <= self.screen.get_width()/2 - 200 + (i % 4)*160 and (i//4)*150+500 <= pos[1] <= (i//4)*150+580:
                pygame.draw.rect(self.screen, [255, 0, 255], [self.screen.get_width()/2 - 280 + (i % 4)*160, (i//4)*150+500, 80, 80], 2)
        # 放在保存按钮上
        self.save.changeColor(pos)

    # 鼠标点击
    def mouse_click(self, pos):
        # 点击返回
        if self.back.isClicked(pos):
            self.father.now_screen = 'menu'
        # 点击棋子
        elif self.screen.get_width()/2-100-self.father.play_screen.man_width <= pos[0] <= self.screen.get_width()/2-100 and 100 <= pos[1] <= 100+self.father.play_screen.man_height and self.choose_man == 'black':
            self.choose_man = 'white'
        elif self.screen.get_width()/2+100 <= pos[0] <= self.screen.get_width()/2+100+self.father.play_screen.man_width and 100 <= pos[1] <= 100+self.father.play_screen.man_height and self.choose_man == 'white':
            self.choose_man = 'black'
        # 点击背景
        elif 200 <= pos[1] <= 400:
            for i in range(len(self.all_bg)):
                if self.screen.get_width()/2 - 550 + i*300 <= pos[0] <= self.screen.get_width()/2 - 350 + i*300:
                    self.choose_bg = self.all_bg[i]
                    break
        # 点击保存
        elif self.save.isClicked(pos):
            self.set_conf()
        # 点击头像
        for i in range(len(self.all_avatar)):
            if self.screen.get_width()/2 - 280 + (i % 4)*160 <= pos[0] <= self.screen.get_width()/2 - 200 + (i % 4)*160 and (i//4)*150+500 <= pos[1] <= (i//4)*150+580:
                self.choose_avatar = self.all_avatar[i]
                break
