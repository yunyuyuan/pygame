import pygame
from random import randint
from gametool.alert import Window
from gametool.GameButton import Button
from json import dump, load
from threading import Thread
from time import sleep
from itertools import combinations
from copy import deepcopy

pygame.init()


class Game(object):
    def __init__(self, father):
        self.father = father
        self.font = pygame.font.SysFont('kaiti', 30, True)
        self.level = 'easy'
        self.num = [9, 9]
        # 开始记录和结束记录
        self.start = False
        self.game_over = False
        self.game_over_alert = None
        self.use_ai = False
        self.fail_pos = [-1, -1]
        # ai是否死猜
        self.death_choose = True
        # ai是否插旗
        self.ai_flag = True
        self.mine_num = 0
        # ai速度
        self.ai_speed = 3
        self.init()

    # 初始化
    def init(self):
        # 坐标和大小
        if self.father.size[0] == 1920:
            self.font = pygame.font.SysFont('kaiti', 25, True)
            multiple = 1
            font_pos_alter = [30, 20]
            self.num_font = pygame.font.SysFont('fangsong', 25, True)
            if self.level == 'easy':
                self.box_size = [88, 88]
                self.border_size = [792, 792]
                self.num = [9, 9]
            elif self.level == 'mid':
                self.box_size = [50, 50]
                self.border_size = [800, 800]
                self.num = [16, 16]
            else:
                self.box_size = [50, 50]
                self.border_size = [1500, 800]
                self.num = [30, 16]
        else:
            self.font = pygame.font.SysFont('kaiti', 20, True)
            multiple = 0.7
            font_pos_alter = [20, 10]
            self.num_font = pygame.font.SysFont('fangsong', 18, True)
            if self.level == 'easy':
                self.box_size = [70, 70]
                self.border_size = [630, 630]
                self.num = [9, 9]
            elif self.level == 'mid':
                self.box_size = [40, 40]
                self.border_size = [640, 640]
                self.num = [16, 16]
            else:
                self.box_size = [33, 33]
                self.border_size = [990, 528]
                self.num = [30, 16]
        # 按钮
        self.back = Button(self.father.screen, '', [self.father.size[0] // 20, self.father.size[1] // 10], mod='back',
                           hover_pic='back_hover', multiple=multiple)
        self.re_play = Button(self.father.screen, '重开', [self.father.size[0] // 18, self.father.size[1] // 5], font_pos_alter=font_pos_alter, mod='button1', multiple=multiple)
        self.ai = Button(self.father.screen, '启动AI', [self.father.size[0] // 18, self.father.size[1] // 3.5], font_pos_alter=[int(font_pos_alter[0]*1.5), font_pos_alter[1]], mod='button1', multiple=multiple)
        # 计时框
        self.timer_box = pygame.image.load('images/timer.png')
        self.timer_box = pygame.transform.scale(self.timer_box, [int(150*multiple), int(150*multiple)])
        self.timer_box_pos = [self.father.size[1]//50, self.father.size[1] // 3]
        self.font_pos = [self.father.size[1]//50+self.timer_box.get_width()//3, self.father.size[1] // 3+self.timer_box.get_height()//2.5]
        self.speed_pos = [10, self.timer_box_pos[1] + self.timer_box.get_height()+10]
        self.rest_pos = [0, self.speed_pos[1]+int(50*multiple)]

        self.box = pygame.transform.scale(pygame.image.load('images/box.png').convert_alpha(), self.box_size)
        self.box_hover = pygame.transform.scale(pygame.image.load('images/box_hover.png').convert_alpha(), self.box_size)
        self.box_sweep = pygame.transform.scale(pygame.image.load('images/box_sweep.png').convert_alpha(), self.box_size)
        self.border = pygame.transform.scale(pygame.image.load('images/size.png').convert_alpha(), self.border_size)
        self.flag = pygame.transform.scale(self.father.flag, self.box_size)
        self.border_pos = [(self.father.size[0] - self.border_size[0])//2, (self.father.size[1] - self.border_size[1])//2]
        # 选项
        self.death_choose_frame = pygame.image.load('images/size.png').convert_alpha()
        self.death_choose_frame.blit(self.father.font.render('是否死猜', False, [0, 0, 0]), [10, 10])
        self.death_choose_frame = pygame.transform.scale(self.death_choose_frame, [int(200*multiple), int(50*multiple)])
        self.flag_choose_frame = pygame.image.load('images/size.png').convert_alpha()
        self.flag_choose_frame.blit(self.father.font.render('是否插旗', False, [0, 0, 0]), [10, 10])
        self.flag_choose_frame = pygame.transform.scale(self.flag_choose_frame, [int(200*multiple), int(50*multiple)])
        self.speed_choose_frame = pygame.image.load('images/size.png').convert_alpha()
        self.speed_choose_frame.blit(self.father.font.render('扫雷速度', False, [0, 0, 0]), [10, 10])
        self.speed_choose_frame = pygame.transform.scale(self.speed_choose_frame, [int(200*multiple), int(50*multiple)])
        self.frame_pos_1 = [self.father.size[1]//50, self.father.size[1] // 2]
        self.frame_pos_2 = [self.father.size[1]//50, self.father.size[1]*13 // 20]
        self.frame_pos_3 = [self.father.size[1]//50, self.father.size[1]*16 // 20]
        # 数字
        for i in range(1, 9):
            exec("self.num_{0} = pygame.transform.scale(pygame.image.load('images/numbers/{0}.png').convert_alpha(), {1})".format(i, [int(self.box_size[0]*0.8), int(self.box_size[0]*0.8)]))
        # 地雷
        self.mine = pygame.transform.scale(self.father.mine, self.box_size)
        self.num_list = [self.num_1, self.num_2, self.num_3, self.num_4, self.num_5, self.num_6, self.num_7, self.num_8]
        self.reload()

    def reload(self):
        self.ai.text = '启动AI'
        # 游戏列表和旗子列表
        self.game_list = [[0 for x in range(self.num[1])] for y in range(self.num[0])]
        self.flag_list = []
        self.mine_num = 0
        # 已经没有未挖块的列表
        self.close_list = []
        self.last_click = [0, 0]
        # 游戏状态
        self.start = False
        self.game_over = False
        self.game_over_alert = None
        self.use_ai = False
        # 死猜和插旗
        if self.father.now_death == 0:
            self.death_choose = False
        else:
            self.death_choose = True
        # 踩雷点
        self.fail_pos = [-1, -1]
        # 计时器
        self.time_event = pygame.USEREVENT + 1
        self.time_count = 0
        pygame.time.set_timer(self.time_event, 100)

    def blit(self):
        for i in range(self.num[0]):
            for j in range(self.num[1]):
                # 画掩盖
                if self.game_list[i][j] == 0 or self.game_list[i][j] >= 10 or self.game_list[i][j] == -2:
                    self.father.screen.blit(self.box, [self.border_pos[0]+i*self.box_size[0], self.border_pos[1]+j*self.box_size[1]])
                # 已被挖
                elif self.game_list[i][j] == -1:
                    self.father.screen.blit(self.box_sweep, [self.border_pos[0]+i*self.box_size[0], self.border_pos[1]+j*self.box_size[1]])
                # 数字
                elif 1 <= self.game_list[i][j] <= 8:
                    self.father.screen.blit(self.box_sweep, [self.border_pos[0]+i*self.box_size[0], self.border_pos[1]+j*self.box_size[1]])
                    self.father.screen.blit(self.num_list[self.game_list[i][j]-1], [self.border_pos[0]+i*self.box_size[0]+5, self.border_pos[1]+j*self.box_size[1]+5])
        if self.fail_pos[0] != -1:
            pygame.draw.rect(self.father.screen, [255, 0, 0], [self.border_pos[0]+self.fail_pos[0]*self.box_size[0],
                                                               self.border_pos[1]+self.fail_pos[1]*self.box_size[1], self.box_size[0], self.box_size[1]], 3)
        # 旗子
        for pos in self.flag_list:
            self.father.screen.blit(self.flag, [self.border_pos[0]+pos[0]*self.box_size[0], self.border_pos[1]+pos[1]*self.box_size[1]])
        # 按钮
        self.back.blit()
        self.re_play.blit()
        self.ai.blit()
        # 计时器
        self.father.screen.blit(self.timer_box, self.timer_box_pos)
        self.father.screen.blit(self.num_font.render(str(self.time_count/10), False, [255, 0, 0]), self.font_pos)
        # 速度和剩余雷
        self.father.screen.blit(self.font.render('AI速度:%d' % self.ai_speed, False, [255, 0, 0]), self.speed_pos)
        self.father.screen.blit(self.font.render('剩余雷数:%d' % (self.mine_num-len(self.flag_list)), False, [50, 255, 0]), self.rest_pos)
        # game over
        if self.game_over:
            # 画出所有的雷
            for i in range(self.num[0]):
                for j in range(self.num[1]):
                    if self.game_list[i][j] == -2:
                        self.father.screen.blit(self.mine, [self.border_pos[0]+i*self.box_size[0], self.border_pos[1]+j*self.box_size[1]])
            if self.game_over_alert:
                self.game_over_alert.blit()
            return

    def hover(self, pos):
        if self.game_over:
            if self.game_over_alert:
                self.game_over_alert.hover(pos)
                return
            self.back.hover(pos)
            self.re_play.hover(pos)
            return
        self.back.hover(pos)
        self.re_play.hover(pos)
        self.ai.hover(pos)
        for i in range(self.num[0]):
            for j in range(self.num[1]):
                if self.border_pos[0] + i * self.box_size[0] <= pos[0] <= self.border_pos[0] + (i+1) * self.box_size[0] and self.border_pos[1] + j * self.box_size[1] <= pos[1] <= self.border_pos[1] + (j+1) * self.box_size[1]:
                    if [i, j] not in self.flag_list:
                        if self.game_list[i][j] == 0 or self.game_list[i][j] >= 10 or self.game_list[i][j] == -2:
                            self.father.screen.blit(self.box_hover, [self.border_pos[0] + i * self.box_size[0], self.border_pos[1] + j * self.box_size[1]])
                    return

    def click(self, pos, btn):
        # 游戏结束，提示界面
        if self.game_over:
            if self.game_over_alert:
                if self.game_over_alert.click(pos) == '重开':
                    self.reload()
                elif self.game_over_alert.click(pos) == '返回':
                    self.game_over_alert = None
                return
            # 游戏结束，可以按重开和返回
            if self.back.click(pos):
                self.father.now_screen = self.father.menu_screen
            elif self.re_play.click(pos):
                self.reload()
            return
        if self.back.click(pos):
            self.father.now_screen = self.father.menu_screen
        elif self.re_play.click(pos):
            self.reload()
        elif self.ai.click(pos):
            if not self.use_ai:
                # 启动AI
                self.ai.text = '关闭ai'
                self.use_ai = True
                self.ai_sweep()
            else:
                # 关闭ai
                self.ai.text = '启动ai'
                self.use_ai = False
        # 计算点击的是哪个块
        if self.border_pos[0] <= pos[0] <= self.border_pos[0]+self.num[0]*self.box_size[0] and self.border_pos[1] <= pos[1] <= self.border_pos[1]+self.num[1]*self.box_size[1]:
            [i, j] = [(pos[0]-self.border_pos[0])//self.box_size[0], (pos[1]-self.border_pos[1])//self.box_size[1]]
            # 点击close_list无效
            if [i, j] not in self.close_list:
                # 左键且不是旗子
                if btn == 0 and [i, j] not in self.flag_list:
                    # 创造游戏
                    if not self.start:
                        self.start = True
                        self.create_list([i, j])
                        self.last_click = [i, j]
                    # 点开方块
                    if self.game_list[i][j] == 0:
                        self.game_list[i][j] = -1
                        # 自动开图
                        self.auto_sweep([i, j])
                        self.last_click = [i, j]
                    # 点击数字
                    elif 1 <= self.game_list[i][j] <= 8:
                        self.double_click([i, j])
                    # 点击隐藏数字
                    elif self.game_list[i][j] >= 10:
                        self.game_list[i][j] = self.game_list[i][j]//10
                        self.last_click = [i, j]
                    # 点击雷
                    elif self.game_list[i][j] == -2:
                        self.fail_pos = [i, j]
                        self.game_over_alert = Window(self.father.screen, [self.father.size[0]//2, self.father.size[1]//2], 'alert1', 'game_over',
                                                      texts=['重开', '返回'], rotate_speed=0)
                        self.update_record()
                        self.game_over = True
                        return 'game over'
                # 右键
                elif btn == 2:
                    if self.game_list[i][j] == -2 or self.game_list[i][j] == 0 or self.game_list[i][j] >= 10:
                        # 插旗
                        if [i, j] not in self.flag_list:
                            self.flag_list.append([i, j])
                        else:
                            # 取消插旗
                            self.flag_list.pop(self.flag_list.index([i, j]))
        # 检查加入close_list
        for i in range(self.num[0]):
            for j in range(self.num[1]):
                if [i, j] not in self.close_list and 1 <= self.game_list[i][j] <= 8:
                    count = 0
                    for around in self.neighbor_box([i, j]):
                        if around in self.flag_list:
                            count += 1
                        elif self.game_list[around[0]][around[1]] == 0 or self.game_list[around[0]][around[1]] == -2 or self.game_list[around[0]][around[1]] >= 10:
                            break
                    else:
                        if count == self.game_list[i][j]:
                            self.close_list.append([i, j])
        # 判断是否赢了
        for i in range(self.num[0]):
            for j in range(self.num[1]):
                if self.game_list[i][j] == 0 or self.game_list[i][j] >= 10:
                    return
        self.game_over_alert = Window(self.father.screen, [self.father.size[0] // 2, self.father.size[1] // 2], 'alert1', 'success',
                                      texts=['重开', '返回'], rotate_speed=0)
        # 检查是否破纪录
        best_record = load(open('record.json', 'r'))[['easy', 'mid', 'hard'].index(self.level)][0]
        if float(best_record) > self.time_count/10:
            self.game_over_alert.load_text('最新记录!用时:' + str(self.time_count / 10) + 's', [self.father.size[0] // 2 - 130,
                                           self.father.size[1] // 2 - 110], text_info=['kaiti', 30, 0])
            # 更新记录
            self.update_record(True, self.time_count/10)
        else:
            self.game_over_alert.load_text('您赢了 用时:' + str(self.time_count / 10) + 's', [self.father.size[0] // 2 - 100,
                                           self.father.size[1] // 2 - 110], text_info=['kaiti', 30, 0])
            # 更新记录
            self.update_record(True)
        self.game_over = True

    def thread_ai(self):
        Thread(target=self.ai_sweep, args=(self.ai_speed/10,)).start()

    # 生成游戏
    def create_list(self, pos):
        if self.level == 'easy':
            self.mine_num = 10
        elif self.level == 'mid':
            self.mine_num = 40
        else:
            self.mine_num = 99
        # 生产雷
        mine_list = []
        while len(mine_list) < self.mine_num:
            new_pos = [randint(0, self.num[0]-1), randint(0, self.num[1]-1)]
            if (new_pos[0] <= pos[0]-2 or new_pos[0] >= pos[0]+2) or (new_pos[1] <= pos[1]-2 or new_pos[1] >= pos[1]+2):
                if new_pos not in mine_list:
                    mine_list.append(new_pos)
        # 放雷
        for i in mine_list:
            self.game_list[i[0]][i[1]] = -2
        # 设置数字
        for i in range(self.num[0]):
            for j in range(self.num[1]):
                if self.game_list[i][j] != -2:
                    count = 0
                    neighbor = self.neighbor_box([i, j])
                    for p in neighbor:
                        if self.game_list[p[0]][p[1]] == -2:
                            count += 1
                    if count > 0:
                        self.game_list[i][j] = count*10

    # 周围八个或更少的方块列表
    def neighbor_box(self, pos):
        return_list = []
        for m in range(-1, 2):
            for n in range(-1, 2):
                if m == 0 and n == 0:
                    continue
                num_pos = [pos[0]+m, pos[1]+n]
                if 0 <= num_pos[0] < self.num[0] and 0 <= num_pos[1] < self.num[1]:
                    return_list.append(num_pos)
        return return_list

    # 对某个坐标周围自动开图
    def auto_sweep(self, pos):
        for pos in self.neighbor_box(pos):
            if self.game_list[pos[0]][pos[1]] >= 10:
                self.game_list[pos[0]][pos[1]] = self.game_list[pos[0]][pos[1]]//10
            elif self.game_list[pos[0]][pos[1]] == 0:
                self.game_list[pos[0]][pos[1]] = -1
                self.auto_sweep(pos)

    # 双击开图
    def double_click(self, pos):
        num = self.game_list[pos[0]][pos[1]]
        count = 0
        # 检查旗子数量
        un_sweep = []
        for i in self.neighbor_box(pos):
            if i in self.flag_list:
                count += 1
            elif self.game_list[i[0]][i[1]] == 0 or self.game_list[i[0]][i[1]] == -2 or self.game_list[i[0]][i[1]] >= 10:
                un_sweep.append(i)
        if count == num:
            for i in un_sweep:
                self.click([self.border_pos[0]+i[0]*self.box_size[0]+2, self.border_pos[1]+i[1]*self.box_size[1]+2], 0)
                self.last_click = i

    # 计时器
    def timer(self, event):
        # 已经开始且没结束，计时
        if event.type == self.time_event and not self.game_over and self.start:
            self.time_count += 1

    # 更新记录
    def update_record(self, win=False, best=None):
        info = load(open('record.json', 'r'))
        current_idx = ['easy', 'mid', 'hard'].index(self.level)
        info[current_idx][1] += 1
        if win:
            info[current_idx][2] += 1
        if best:
            info[current_idx][0] = best
        dump(info, open('record.json', 'w'))

    def cal_around(self, pos):
        return_x = []
        return_y = []
        for i in range(max(pos[0], self.num[0]-pos[0])+1):
            if i == 0:
                return_x.append(i)
            else:
                return_x.extend([i, -i])
        return_1 = []
        for i in return_x:
            if 0 <= pos[0] + i <= (self.num[0]-1):
                return_1.append(i)
        for i in range(max(pos[1], self.num[0]-pos[1])+1):
            if i == 0:
                return_y.append(i)
            else:
                return_y.extend([i, -i])
        return_2 = []
        for i in return_y:
            if 0 <= pos[1] + i <= (self.num[1]-1):
                return_2.append(i)
        return [return_1, return_2]

    # ai扫雷
    def ai_sweep(self, delay=0.0):
        if delay > 0.0:
            sleep(delay)
        if self.use_ai and not self.game_over:
            # 开图
            if not self.start:
                pos = [self.border_pos[0]+self.num[0]*self.box_size[0]//2, self.border_pos[1]+self.num[1]*self.box_size[1]//2]
                self.click(pos, 0)
            last_guess = 0
            # 从last_click周围开始检查
            around = self.cal_around(self.last_click)
            for ii in around[0]:
                for jj in around[1]:
                    [i, j] = [self.last_click[0]+ii, self.last_click[1]+jj]
                    # 对已挖开且不在close_list的的数字
                    if 1 <= self.game_list[i][j] <= 8 and [i, j] not in self.close_list:
                        unsweep_list, flag_list, all_possible, can_possible, num_list = self.cal_([i, j])
                        # 设置猜雷
                        if can_possible and self.death_choose:
                            if can_possible[0]:
                                if self.game_list[can_possible[0][0][0]][can_possible[0][0][1]] in [0, -2] or self.game_list[can_possible[0][0][0]][can_possible[0][0][1]] >= 10:
                                    last_guess = can_possible[0][0]
                        # ################################## 若数字和周围插旗数相同,剩下的都不是雷
                        if len(flag_list) == self.game_list[i][j] and len(unsweep_list) > 0:
                            self.click([self.border_pos[0]+i*self.box_size[0]+2, self.border_pos[1]+j*self.box_size[1]+2], 0)
                            self.thread_ai()
                            return
                        if unsweep_list:
                            # 周围剩下的雷数量
                            rest_mine_num = self.game_list[i][j] - len(flag_list)
                            # ################################### 若雷和周围的块数量相同,全部是雷
                            if len(unsweep_list) == rest_mine_num:
                                for pos in unsweep_list:
                                    if pos not in self.flag_list:
                                        self.flag_list.append(pos)
                                #     self.click([self.border_pos[0]+pos[0]*self.box_size[0]+2, self.border_pos[1]+pos[1]*self.box_size[1]+2], 2)
                                # self.thread_ai()
                                # return
                            # ############################## can_possible全不包含的,肯定不是雷
                            no_mine = deepcopy(unsweep_list)
                            for mine in unsweep_list:
                                for line in can_possible:
                                    if mine in line:
                                        no_mine.remove(mine)
                                        break
                            if no_mine:
                                for pos in no_mine:
                                    self.click([self.border_pos[0]+pos[0]*self.box_size[0]+2, self.border_pos[1]+pos[1]*self.box_size[1]+2], 0)
                                self.thread_ai()
                                return
                            # ############################# can_possible都包含的,肯定是雷
                            must_mine = deepcopy(unsweep_list)
                            for mine in unsweep_list:
                                for line in can_possible:
                                    if mine not in line:
                                        must_mine.remove(mine)
                                        break
                            if must_mine:
                                for pos in must_mine:
                                    if pos not in self.flag_list:
                                        self.flag_list.append(pos)
                                #     self.click([self.border_pos[0]+pos[0]*self.box_size[0]+2, self.border_pos[1]+pos[1]*self.box_size[1]+2], 2)
                                # self.thread_ai()
                                # return
                            # 逻辑判断
                            can_possible.sort()
                            for line in range(len(can_possible)):
                                can_possible[line].sort()
                            ten_list = []
                            for pos in num_list:
                                if not (pos[0] - i != 0 and pos[1] - j != 0):
                                    ten_list.append(pos)
                            for pos in ten_list:
                                unsweep_list_, flag_list_, all_possible_, can_list, num_list_ = self.cal_(pos)
                                can_list.sort()
                                for line in range(len(can_list)):
                                    can_list[line].sort()
                                # 交集
                                and_list = []
                                for a in can_possible:
                                    if a in can_list:
                                        and_list.append(a)
                                # 有雷的地方
                                mine_list = []
                                for line in can_list:
                                    for item in line:
                                        if item not in mine_list:
                                            mine_list.append(item)
                                # ###################### 两十字相邻块的can_list差集不是雷
                                if len(can_list[0]) == (self.game_list[i][j]-len(flag_list)) and and_list == can_list and len(can_possible) > len(can_list):
                                    no_mine_list = []
                                    for line in can_possible:
                                        if line not in can_list:
                                            for item in line:
                                                if item not in no_mine_list and item not in mine_list:
                                                    no_mine_list.append(item)
                                    if no_mine_list:
                                        for position in no_mine_list:
                                            self.click([self.border_pos[0] + position[0] * self.box_size[0] + 2,
                                                        self.border_pos[1] + position[1] * self.box_size[1] + 2], 0)
                                        self.thread_ai()
                                        return
                                # ######################### 相邻块的can_list全部包含了自己can_possible的多种情况,则剩下的情况不是雷
                                if len(can_list[0]) >= len(can_possible[0]):
                                    # 对can_list的所有情况，和can_possible的每种求交集，至少有一个满足则满足
                                    count = 0
                                    for line in can_list:
                                        for mom in can_possible:
                                            for item in mom:
                                                if item not in line:
                                                    break
                                            else:
                                                count += 1
                                                break
                                    # 若count等于len(can_list)说明全包含
                                    if count == len(can_list):
                                        maybe_no_mine = []
                                        for mom in can_possible:
                                            for item in mom:
                                                for line in can_list:
                                                    if item in line:
                                                        break
                                                else:
                                                    if item not in maybe_no_mine:
                                                        maybe_no_mine.append(item)
                                        # 剩下的不是雷
                                        if maybe_no_mine:
                                            for no_mine in maybe_no_mine:
                                                self.click([self.border_pos[0] + no_mine[0] * self.box_size[0] + 2,
                                                            self.border_pos[1] + no_mine[1] * self.box_size[1] + 2], 0)
                                            self.thread_ai()
                                            return
            # 最后的情况,flag_list=雷数目
            if len(self.flag_list) == self.mine_num:
                for i in range(self.num[0]):
                    for j in range(self.num[1]):
                        if [i, j] not in self.flag_list:
                            if self.game_list[i][j] == 0 or self.game_list[i][j] == -2 or self.game_list[i][j] >= 10:
                                self.click([self.border_pos[0] + i * self.box_size[0] + 2,
                                            self.border_pos[1] + j * self.box_size[1] + 2], 0)
                return
            # ai扫雷失败
            # 猜雷
            if self.death_choose:
                if not last_guess:
                    for i in range(self.num[0]):
                        for j in range(self.num[1]):
                            if self.game_list[i][j] == 0 or self.game_list[i][j] == -2 or self.game_list[i][j] >= 10:
                                last_guess = [i, j]
                self.click([self.border_pos[0] + last_guess[0] * self.box_size[0] + 2,
                            self.border_pos[1] + last_guess[1] * self.box_size[1] + 2], 0)
                self.thread_ai()
                return
            self.thread_ai()
            return

    # 计算unsweep和can
    def cal_(self, pos_):
        unsweep_list = []
        flag_list = []
        # 周围是数字的块
        num_list = []
        neighbor = self.neighbor_box([pos_[0], pos_[1]])
        for pos in neighbor:
            if 1 <= self.game_list[pos[0]][pos[1]] <= 8:
                num_list.append(pos)
            if pos not in self.flag_list:
                if self.game_list[pos[0]][pos[1]] == 0 or self.game_list[pos[0]][pos[1]] == -2 or \
                        self.game_list[pos[0]][pos[1]] >= 10:
                    unsweep_list.append(pos)
            else:
                flag_list.append(pos)
        all_possible = []
        can_possible = []
        rest_mine_num = self.game_list[pos_[0]][pos_[1]] - len(flag_list)
        for poss in iter(combinations(unsweep_list, rest_mine_num)):
            all_possible.append(list(poss))
        # 判断周围数字块是否满足情况
        for mines in all_possible:
            # 虚拟插旗
            virtual_flag_list = deepcopy(self.flag_list)
            virtual_flag_list.extend(mines)
            # 对周围的数字，检查虚拟插旗数是否比他大
            for num_pos in num_list:
                count = 0
                around = self.neighbor_box(num_pos)
                for box in around:
                    if box in virtual_flag_list:
                        count += 1
                # 插旗数比数字大，不合理
                if count > self.game_list[num_pos[0]][num_pos[1]]:
                    break
            else:
                can_possible.append(mines)
        return unsweep_list, flag_list, all_possible, can_possible, num_list
