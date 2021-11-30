from 小工具.gametool.GameButton import Button
from 小工具.gametool.alert import Window
from requests import post
import pygame
from threading import Thread
from json import loads
from copy import deepcopy


# 游戏界面
class Play(object):
    def __init__(self, father, surface):
        self.screen = surface
        self.father = father
        self.font = pygame.font.SysFont('kaiti', 20)
        self.font1 = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 30)
        self.font2 = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 25)
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()
        self.checkerboard_pos = [500, 100]
        # 棋子
        self.black_man = pygame.image.load('./images/black_man.png').convert_alpha()
        self.white_man = pygame.image.load('./images/white_man.png').convert_alpha()
        self.clock = pygame.transform.scale(pygame.image.load('./images/clock.png').convert_alpha(), [50, 50])

        # 棋子的长宽
        self.man_width = self.black_man.get_width()
        self.man_height = self.black_man.get_height()
        # 匹配状态
        self.matched = False
        self.has_give_up = False
        # 下棋状态
        self.game_info = []
        self.set_condi = False
        self.is_first = False
        # 所有棋子
        self.man_list = [[], []]
        # 游戏结果
        self.result = None
        # 退出按钮
        self.back = Button(self.screen, '退出', [self.checkerboard_pos[0] +1200,self.checkerboard_pos[1]+300], font_pos_alter=[40, 20])

        self.enemy_avatar = pygame.image.load('./images/user_avatar/mouse.png').convert()
        # 计时器事件
        self.time = 20
        self.record_time = False
        self.time_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.time_event, 1000)

    # 计时器
    def timer(self, event):
        if event.type == self.time_event and self.record_time:
            self.time -= 1
            # 超时未下
            if self.set_condi and self.time == 0:
                self.send_pos([-1, -1])

    # 判断胜负
    def judge(self):
        if not self.is_first:
            man_list = deepcopy([self.man_list[1], self.man_list[0]])
        else:
            man_list = deepcopy(self.man_list)
        for pos in man_list[0]:
            if ([pos[0]+1,pos[1]+1] in man_list[0] and [pos[0]+2,pos[1]+2] in man_list[0] and [pos[0]+3,pos[1]+3] in man_list[0] and [pos[0]+4,pos[1]+4] in man_list[0])\
                or ([pos[0]+1,pos[1]-1] in man_list[0] and [pos[0]+2,pos[1]-2] in man_list[0] and [pos[0]+3,pos[1]-3] in man_list[0] and [pos[0]+4,pos[1]-4] in man_list[0])\
                or ([pos[0] + 1, pos[1]] in man_list[0] and [pos[0]+2,pos[1]] in man_list[0] and [pos[0]+3,pos[1]] in man_list[0] and [pos[0]+4,pos[1]] in man_list[0]) \
                    or ([pos[0], pos[1] + 1] in man_list[0] and [pos[0],pos[1]+2] in man_list[0] and [pos[0],pos[1]+3] in man_list[0] and [pos[0],pos[1]+4] in man_list[0]):
                self.father.alert_window = Window(self.screen,
                                                  [self.screen.get_width() / 2, self.screen.get_height() / 2], 'alert1',
                                                  '', texts=['确定'], rotate_speed=0)
                self.father.alert_mod = 'result'
                self.father.alert_window.load_text('您赢了', [1000, 550])
                self.result = 'success'
                self.record_time = False
                return 'success'
        for pos in man_list[1]:
            if ([pos[0]+1,pos[1]+1] in man_list[1] and [pos[0]+2,pos[1]+2] in man_list[1] and [pos[0]+3,pos[1]+3] in man_list[1] and [pos[0]+4,pos[1]+4] in man_list[1]) \
                    or ([pos[0] + 1, pos[1] - 1] in man_list[1] and [pos[0] + 2, pos[1] - 2] in man_list[1] and [pos[0] + 3,pos[1] - 3] in man_list[1] and [pos[0] + 4, pos[1] - 4] in man_list[1]) \
                    or ([pos[0] + 1, pos[1]] in man_list[1] and [pos[0]+2,pos[1]] in man_list[1] and [pos[0]+3,pos[1]] in man_list[1] and [pos[0]+4,pos[1]] in man_list[1]) \
                    or ([pos[0], pos[1] + 1] in man_list[1] and [pos[0],pos[1]+2] in man_list[1] and [pos[0],pos[1]+3] in man_list[1] and [pos[0],pos[1]+4] in man_list[1]):
                self.father.alert_window = Window(self.screen,
                                                  [self.screen.get_width() / 2, self.screen.get_height() / 2], 'alert1',
                                                  '', texts=['确定'], rotate_speed=0)
                self.father.alert_mod = 'result'
                self.father.alert_window.load_text('您输了', [1000, 550])
                self.result = 'fail'
                self.record_time = False
                return 'fail'

    # 匹配函数
    def match(self, name):
        json = {
            'name': name,
        }
        response = post(self.father.server_ip+'match', json=json, timeout=25)
        if response.ok:
            if response.content.decode('utf-8') != 'no game':
                # 匹配成功
                self.father.alert_window = None
                self.matched = True
                self.game_info = loads(response.content.decode('utf-8'))
                self.enemy_avatar = pygame.transform.scale(pygame.image.load('./images/user_avatar/%s.png' % eval(self.game_info[1][1])[2]).convert(), [100, 100])
                # 先手下棋
                if self.game_info[2] == 0:
                    self.record_time = True
                    self.set_condi = True
                    self.is_first = True
                else:
                    self.go_recv()
            elif self.father.alert_window and not self.has_give_up:
                self.father.alert_window.load_alert('', 0)
                self.father.alert_window.load_text('匹配超时！', [self.father.alert_window.pos[0]+100, self.father.alert_window.pos[1]+100])

    # 取消匹配
    def give_up_match(self):
        json = {
            'name': self.father.user_num,
        }
        post(self.father.server_ip+'give_up_match', json=json)
        self.has_give_up = True

    # 发送下棋坐标
    def send_pos(self, pos):
        json = {
            'game_id': self.game_info[0],
            'pos': pos,
            'is_first': self.is_first,
        }
        response = post(self.father.server_ip+'send', json=json)
        # 置状态为等待并刷新棋子
        if response.ok:
            self.set_condi = False
            if pos == [-1, -1]:
                pass
            elif self.is_first:
                self.man_list[0].append(pos)
            else:
                self.man_list[1].append(pos)
            if not self.judge():
                # 等待接受
                self.go_recv()

    # 后台匹配
    def go_match(self):
        # 匹配状态
        self.matched = False
        # 下棋状态
        self.game_info = []
        self.set_condi = False
        self.is_first = False
        # 所有棋子
        self.man_list = [[], []]
        Thread(target=self.match, args=[self.father.user_num, ]).start()

    # 后台接受
    def go_recv(self):
        Thread(target=self.recv).start()

    # 接受
    def recv(self):
        json = {
            'game_id': self.game_info[0],
            'is_first': self.is_first,
        }
        print('准备接受')
        # 为对方计时
        self.time = 20
        self.record_time = True
        response = post(self.father.server_ip+'recv', json=json, timeout=25)
        # 置状态为下棋并刷新棋子
        if response.ok:
            # 超时算弃权
            if response.content.decode('utf-8') == 'timeout':
                print('对方弃权')
            else:
                pos = loads(response.content.decode('utf-8'))
                print('接受', pos)
                if pos == [-1, -1]:
                    pass
                elif self.is_first:
                    self.man_list[1].append(eval(pos))
                else:
                    self.man_list[0].append(eval(pos))
                self.judge()
            # 为自己计时
            self.time = 20
            self.record_time = True
            self.set_condi = True

    # 画棋盘和按钮,棋子
    def draw_stuff(self):
        # 按钮
        self.back.drawButton()
        # 棋盘背景
        if self.father.set_screen.bg_pic:
            self.screen.blit(self.father.set_screen.bg_pic, [self.checkerboard_pos[0]-75, self.checkerboard_pos[1]-75])
        # 棋盘
        for i in range(15):
            pygame.draw.line(self.screen, [0, 0, 0], [self.checkerboard_pos[0], self.checkerboard_pos[1]+i*60], [self.checkerboard_pos[0]+840, self.checkerboard_pos[1]+i*60], 2)
            pygame.draw.line(self.screen, [0, 0, 0], [self.checkerboard_pos[0]+i*60, self.checkerboard_pos[1]], [self.checkerboard_pos[0]+i*60, self.checkerboard_pos[1]+840], 2)
        if self.game_info:
            # 显示对手信息
            self.screen.blit(self.font1.render(str(self.game_info[1][0]), False, [0, 0, 0]), [110, 300])
            self.screen.blit(self.enemy_avatar, [100, 200])
            if not self.result:
                # 时钟
                col = [0, 0, 0]
                if self.time <= 5:
                    col = [200, 0, 0]
                if self.set_condi:
                    # 轮到自己
                    self.screen.blit(self.font2.render(str(self.time), False, col), [240, 680])
                    self.screen.blit(self.clock, [230, 625])
                else:
                    # 轮到对方
                    self.screen.blit(self.font2.render(str(self.time), False, col), [240, 280])
                    self.screen.blit(self.clock, [230, 225])
            # 自己信息
            self.screen.blit(self.font1.render(str(self.father.set_screen.name), False, [0, 0, 0]), [110, 700])
            self.screen.blit(self.father.set_screen.avatar_pic, [100, 600])
        # 画存在的棋子
        if not self.is_first:
            man_list = deepcopy([self.man_list[1], self.man_list[0]])
        else:
            man_list = deepcopy(self.man_list)
        # 己方
        for pos in man_list[0]:
            self.screen.blit(eval("self.%s_man" % self.father.set_screen.choose_man), [pos[0]*60+self.checkerboard_pos[0]-self.man_width//2, pos[1]*60+self.checkerboard_pos[1]-self.man_height//2])
        # 对方
        for pos in man_list[1]:
            if self.father.set_screen.choose_man == 'white':
                man = self.black_man
            else:
                man = self.white_man
            self.screen.blit(man, [pos[0]*60+self.checkerboard_pos[0]-self.man_width//2, pos[1]*60+self.checkerboard_pos[1]-self.man_height//2])

    # 鼠标悬浮
    def mouse_hover(self, pos):
        # 按钮
        self.back.changeColor(pos)
        # 下棋状态,鼠标放在棋盘上方时鼠标改变为棋子
        if not self.result and self.set_condi and (self.checkerboard_pos[0] - 30) <= pos[0] <= (self.checkerboard_pos[0] + 870) and (self.checkerboard_pos[1] - 30) <= pos[1] <= (self.checkerboard_pos[1] + 870):
            # 改变鼠标
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
            # 在鼠标处画棋子
            self.screen.blit(eval("self.%s_man" % self.father.set_screen.choose_man), [pos[0] - self.man_width//2, pos[1] - self.man_height//2])
            # 画出预填框
            # 模糊度
            if 15 < ((pos[0] - self.checkerboard_pos[0] + 30) % 60) < 45 and 15 < ((pos[1] - self.checkerboard_pos[1] + 30) % 60) < 45:
                xy_pos = [(pos[0] - self.checkerboard_pos[0] + 30) // 60,
                           (pos[1] - self.checkerboard_pos[1] + 30) // 60]
                set_pos = [((pos[0] - self.checkerboard_pos[0] + 30)//60)*60+self.checkerboard_pos[0], ((pos[1] - self.checkerboard_pos[1] + 30)//60)*60+self.checkerboard_pos[1]]
                if xy_pos not in self.man_list[0] and set_pos not in self.man_list[1]:
                    pygame.draw.line(self.screen, [255, 0, 0], [set_pos[0] - 30, set_pos[1] - 30],
                                     [set_pos[0] - 30, set_pos[1] - 15], 5)
                    pygame.draw.line(self.screen, [255, 0, 0], [set_pos[0] - 30, set_pos[1] - 30],
                                     [set_pos[0] - 15, set_pos[1] - 30], 5)
                    pygame.draw.line(self.screen, [255, 0, 0], [set_pos[0] - 30, set_pos[1] + 30],
                                     [set_pos[0] - 30, set_pos[1] + 15], 5)
                    pygame.draw.line(self.screen, [255, 0, 0], [set_pos[0] - 30, set_pos[1] + 30],
                                     [set_pos[0] - 15, set_pos[1] + 30], 5)
                    pygame.draw.line(self.screen, [255, 0, 0], [set_pos[0] + 30, set_pos[1] - 30],
                                     [set_pos[0] + 30, set_pos[1] - 15], 5)
                    pygame.draw.line(self.screen, [255, 0, 0], [set_pos[0] + 30, set_pos[1] - 30],
                                     [set_pos[0] + 15, set_pos[1] - 30], 5)
                    pygame.draw.line(self.screen, [255, 0, 0], [set_pos[0] + 30, set_pos[1] + 30],
                                     [set_pos[0] + 30, set_pos[1] + 15], 5)
                    pygame.draw.line(self.screen, [255, 0, 0], [set_pos[0] + 30, set_pos[1] + 30],
                                     [set_pos[0] + 15, set_pos[1] + 30], 5)
        else:
            # 还原鼠标
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

    # 鼠标点击
    def mouse_click(self, pos):
        # 轮到下棋
        if not self.result and self.set_condi and (self.checkerboard_pos[0] - 30) <= pos[0] <= (self.checkerboard_pos[0] + 870) and (self.checkerboard_pos[1] - 30) <= pos[1] <= (self.checkerboard_pos[1] + 870):
            # 下棋
            if 15 < ((pos[0] - self.checkerboard_pos[0] + 30) % 60) < 45 and 15 < (
                    (pos[1] - self.checkerboard_pos[1] + 30) % 60) < 45:
                set_pos = [(pos[0] - self.checkerboard_pos[0] + 30) // 60,
                           (pos[1] - self.checkerboard_pos[1] + 30) // 60]
                # 发送给服务器
                print('发送',set_pos)
                if set_pos not in self.man_list[0] and set_pos not in self.man_list[1]:
                    self.send_pos(set_pos)
        # 点击退出
        if self.back.isClicked(pos):
            # 提前退出
            if not self.result:
                self.father.alert_window = Window(self.screen,
                                                  [self.screen.get_width() / 2, self.screen.get_height() / 2], 'alert1',
                                                  '', texts=['确定', '取消'], rotate_speed=0)
                self.father.alert_mod = 'end_game'
                self.father.alert_window.load_text('确定提前退出？这将会判负并记录', [self.screen.get_width() / 2-200, self.screen.get_height() / 2-100])
            else:
                self.father.now_screen = 'menu'

