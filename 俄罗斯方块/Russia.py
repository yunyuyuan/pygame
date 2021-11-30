import pygame
import copy
from pygame.locals import *
from sys import exit
import random
from threading import Thread

pygame.init()
background = './background.jpg'
record_file_path = './record.txt'
box = './box.png'
music = './BGM.mp3'
# 打开文件
record_file = open(record_file_path, 'r')
record_list = eval(record_file.read())
record_file.close()
ok_bg = 0


class Russia(object):
    # 初始化背景
    def init_screen(self):
        self.screen = pygame.display.set_mode([1920, 1080], pygame.FULLSCREEN, 32)
        global ok_bg
        ok_bg = 1

    def __init__(self, color=0):
        self.de_color = color
        # 初始化屏幕
        if ok_bg == 0:
            self.init_screen()
        self.bg_picture = pygame.image.load(background).convert()
        self.box_picture = pygame.image.load(box).convert_alpha()
        pygame.mixer_music.load(music)
        pygame.mixer_music.play(loops=100)
        pygame.mixer_music.set_volume(0.3)
        # 初始化字体
        self.my_font = pygame.font.SysFont('kaiti', 30, True, True)
        # 初始化得分
        self.my_count = 0
        # 初始化边界矩形列表
        self.border_fixed_rec = []
        # 初始化第一个块
        self.next_box = self.choice(random.randint(1, 7))
        # 初始化颜色
        if color == 0:
            c = [random.randint(10, 245), random.randint(10, 245), random.randint(10, 245)]
        else:
            c = color
        self.rec_1_next = c
        self.rec_2_next = c
        self.rec_3_next = c
        self.rec_4_next = c
        # 下边界
        for x in range(15):
            self.border_fixed_rec.append([682+x*30, 938, 30, 30])
        # 左右边界
        for y in range(33):
            self.border_fixed_rec.append([651, 9+y*30, 30, 30])
            self.border_fixed_rec.append([1132, 9+y*30, 30, 30])
        # 累积块
        self.accumulate_list = []
        # 暂停键
        self.pause = 0
        # 创建矩形
        self.create_new()
        # 时间标志
        self.time_record = 0
        # 变形次数标志
        self.change_record = 0
        # 游戏结束标志
        self.end = 0
        # 暂停标志
        self.pause = 0
        # 等级
        self.level = 1
        # 重新开始方框和显示格子方框和暂停和打开背景音乐
        self.restart_box = pygame.rect.Rect(1540, 450, 130, 50)
        self.show_lines_box = pygame.rect.Rect(200, 350, 100, 30)
        self.pause_box = pygame.rect.Rect(200, 400, 100, 30)
        self.music_box = pygame.rect.Rect(1550, 600, 100, 30)
        # 显示格子
        self.show_lines = 1
        # RGB颜色
        self.lines_color1 = 255
        self.lines_color2 = 0
        self.lines_color3 = 0
        # 暂停标志
        self.pause = -1
        # 快速下落标志
        self.down_fast = 0
        # 播放音乐标志
        self.stop_music = 0
        self.mix_color = 1

    # 变形
    def change(self):
        # 三叉
        if isinstance(self.now_box, Trig):
            # 判断是否能变形
            if self.change_record == 0:
                for rect in self.border_fixed_rec:
                    next_x = [self.rec_3[0] + 30, self.rec_3[1] + 30, 30, 30]
                    if pygame.rect.Rect(next_x).colliderect(rect):
                        return
                self.rec_3[0] += 30
                self.rec_3[1] += 30
                self.change_record = 1
            elif self.change_record == 1:
                for rect in self.border_fixed_rec:
                    next_x = [self.rec_1[0] - 30, self.rec_1[1] + 30, 30, 30]
                    if pygame.rect.Rect(next_x).colliderect(rect):
                        return
                self.rec_1[0] -= 30
                self.rec_1[1] += 30
                self.change_record = 2
            elif self.change_record == 2:
                for rect in self.border_fixed_rec:
                    next_x = [self.rec_4[0] - 30, self.rec_4[1] - 30, 30, 30]
                    if pygame.rect.Rect(next_x).colliderect(rect):
                        return
                self.rec_4[0] -= 30
                self.rec_4[1] -= 30
                self.change_record = 3
            else:
                for rect in self.border_fixed_rec:
                    next_x = [self.rec_3[0] + 30, self.rec_3[1] - 30, 30, 30]
                    if pygame.rect.Rect(next_x).colliderect(rect):
                        return
                self.rec_1[0] += 30
                self.rec_1[1] -= 30
                self.rec_3[0] -= 30
                self.rec_3[1] -= 30
                self.rec_4[0] += 30
                self.rec_4[1] += 30
                self.change_record = 0
        # 直线
        if isinstance(self.now_box, Beeline):
            # 判断是否能变形
            if self.change_record == 0:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0] - 30, self.rec_1[1] + 30, 30, 30]
                    next_x2 = [self.rec_3[0] + 30, self.rec_3[1] - 30, 30, 30]
                    next_x3 = [self.rec_4[0] + 60, self.rec_4[1] - 60, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(rect) or \
                            pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[0] -= 30
                self.rec_1[1] += 30
                self.rec_3[0] += 30
                self.rec_3[1] -= 30
                self.rec_4[0] += 60
                self.rec_4[1] -= 60
                self.change_record = 1
            else:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0] + 30, self.rec_1[1] - 30, 30, 30]
                    next_x2 = [self.rec_3[0] - 30, self.rec_3[1] + 30, 30, 30]
                    next_x3 = [self.rec_4[0] - 60, self.rec_4[1] + 60, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(rect) or \
                            pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[0] += 30
                self.rec_1[1] -= 30
                self.rec_3[0] -= 30
                self.rec_3[1] += 30
                self.rec_4[0] -= 60
                self.rec_4[1] += 60
                self.change_record = 0
        # 左直
        if isinstance(self.now_box, LBeeline):
            # 判断是否能变形
            if self.change_record == 0:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0] + 60, self.rec_1[1], 30, 30]
                    next_x2 = [self.rec_3[0] + 30, self.rec_3[1] - 30, 30, 30]
                    next_x3 = [self.rec_4[0] - 30, self.rec_4[1] + 30, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(rect) or \
                            pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[0] += 60
                self.rec_3[0] += 30
                self.rec_3[1] -= 30
                self.rec_4[0] -= 30
                self.rec_4[1] += 30
                self.change_record = 1
            elif self.change_record == 1:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0], self.rec_1[1] + 60, 30, 30]
                    next_x2 = [self.rec_3[0] + 30, self.rec_3[1] + 30, 30, 30]
                    next_x3 = [self.rec_4[0] - 30, self.rec_4[1] - 30, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(rect) or \
                            pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[1] += 60
                self.rec_3[0] += 30
                self.rec_3[1] += 30
                self.rec_4[0] -= 30
                self.rec_4[1] -= 30
                self.change_record = 2
            elif self.change_record == 2:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0] - 60, self.rec_1[1], 30, 30]
                    next_x2 = [self.rec_3[0] - 30, self.rec_3[1] + 30, 30, 30]
                    next_x3 = [self.rec_4[0] + 30, self.rec_4[1] - 30, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(rect) or \
                            pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[0] -= 60
                self.rec_3[0] -= 30
                self.rec_3[1] += 30
                self.rec_4[0] += 30
                self.rec_4[1] -= 30
                self.change_record = 3
            else:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0], self.rec_1[1] - 60, 30, 30]
                    next_x2 = [self.rec_3[0] - 30, self.rec_3[1] - 30, 30, 30]
                    next_x3 = [self.rec_4[0] + 30, self.rec_4[1] + 30, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(rect) or \
                            pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[1] -= 60
                self.rec_3[0] -= 30
                self.rec_3[1] -= 30
                self.rec_4[0] += 30
                self.rec_4[1] += 30
                self.change_record = 0
        # 右直
        if isinstance(self.now_box, RBeeline):
            # 判断是否能变形
            if self.change_record == 0:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0], self.rec_1[1] + 60, 30, 30]
                    next_x2 = [self.rec_3[0] + 30, self.rec_3[1] - 30, 30, 30]
                    next_x3 = [self.rec_4[0] - 30, self.rec_4[1] + 30, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(
                            rect) or pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[1] += 60
                self.rec_3[0] += 30
                self.rec_3[1] -= 30
                self.rec_4[0] -= 30
                self.rec_4[1] += 30
                self.change_record = 1
            elif self.change_record == 1:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0] - 60, self.rec_1[1], 30, 30]
                    next_x2 = [self.rec_3[0] + 30, self.rec_3[1] + 30, 30, 30]
                    next_x3 = [self.rec_4[0] - 30, self.rec_4[1] - 30, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(
                            rect) or pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[0] -= 60
                self.rec_3[0] += 30
                self.rec_3[1] += 30
                self.rec_4[0] -= 30
                self.rec_4[1] -= 30
                self.change_record = 2
            elif self.change_record == 2:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0], self.rec_1[1] - 60, 30, 30]
                    next_x2 = [self.rec_3[0] - 30, self.rec_3[1] + 30, 30, 30]
                    next_x3 = [self.rec_4[0] + 30, self.rec_4[1] - 30, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(
                            rect) or pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[1] -= 60
                self.rec_3[0] -= 30
                self.rec_3[1] += 30
                self.rec_4[0] += 30
                self.rec_4[1] -= 30
                self.change_record = 3
            else:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0] + 60, self.rec_1[1], 30, 30]
                    next_x2 = [self.rec_3[0] - 30, self.rec_3[1] - 30, 30, 30]
                    next_x3 = [self.rec_4[0] + 30, self.rec_4[1] + 30, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(
                            rect) or pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[0] += 60
                self.rec_3[0] -= 30
                self.rec_3[1] -= 30
                self.rec_4[0] += 30
                self.rec_4[1] += 30
                self.change_record = 0
        # 左梯
        if isinstance(self.now_box, LLadder):
            # 判断是否能变形
            if self.change_record == 0:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0] + 30, self.rec_1[1] + 30, 30, 30]
                    next_x2 = [self.rec_3[0] + 60, self.rec_3[1], 30, 30]
                    next_x3 = [self.rec_4[0] - 30, self.rec_4[1] + 30, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(
                            rect) or pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[0] += 30
                self.rec_1[1] += 30
                self.rec_3[0] += 60
                self.rec_4[0] -= 30
                self.rec_4[1] += 30
                self.change_record = 1
            else:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0] - 30, self.rec_1[1] - 30, 30, 30]
                    next_x2 = [self.rec_3[0] - 60, self.rec_3[1], 30, 30]
                    next_x3 = [self.rec_4[0] + 30, self.rec_4[1] - 30, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(
                            rect) or pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[0] -= 30
                self.rec_1[1] -= 30
                self.rec_3[0] -= 60
                self.rec_4[0] += 30
                self.rec_4[1] -= 30
                self.change_record = 0
        # 右梯
        if isinstance(self.now_box, RLadder):
            # 判断是否能变形
            if self.change_record == 0:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0] + 30, self.rec_1[1] + 30, 30, 30]
                    next_x2 = [self.rec_3[0] + 30, self.rec_3[1] - 30, 30, 30]
                    next_x3 = [self.rec_4[0], self.rec_4[1] + 60, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(
                            rect) or pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[0] += 30
                self.rec_1[1] += 30
                self.rec_3[0] += 30
                self.rec_3[1] -= 30
                self.rec_4[1] += 60
                self.change_record = 1
            else:
                for rect in self.border_fixed_rec:
                    next_x1 = [self.rec_1[0] - 30, self.rec_1[1] - 30, 30, 30]
                    next_x2 = [self.rec_3[0] - 30, self.rec_3[1] + 30, 30, 30]
                    next_x3 = [self.rec_4[0], self.rec_4[1] - 60, 30, 30]
                    if pygame.rect.Rect(next_x1).colliderect(rect) or pygame.rect.Rect(next_x2).colliderect(
                            rect) or pygame.rect.Rect(next_x3).colliderect(rect):
                        return
                self.rec_1[0] -= 30
                self.rec_1[1] -= 30
                self.rec_3[0] -= 30
                self.rec_3[1] += 30
                self.rec_4[1] -= 60
                self.change_record = 0

    # 左右移动
    def transverse(self, how):
        for rec in self.border_fixed_rec:
            for x in self.recs:
                # 判断是否碰壁
                if int(how) == 1:
                    next_x = [x[0]-30, x[1], 30, 30]
                else:
                    next_x = [x[0]+30, x[1], 30, 30]
                if pygame.rect.Rect(next_x).colliderect(rec):
                    return
        for x in self.recs:
            if int(how) == 1:
                x[0] -= 30
            else:
                x[0] += 30

    # 下落
    def move_down(self):
        for rec in self.border_fixed_rec:
            for x in self.recs:
                # 判断是否到底
                next_x = [x[0], x[1] + 1, 30, 30]
                if pygame.rect.Rect(next_x).colliderect(rec):
                    self.fix()
                    return
        for x in self.recs:
            x[1] += self.level

    # 瞬间下落
    def go_fast(self):
        my_lis = []
        for x in self.recs:
            if x[0] not in my_lis:
                my_lis.append(x[0])
        border_lis = []
        for rec in self.border_fixed_rec:
            if rec[0] in my_lis:
                border_lis.append(rec)
        border_lis.sort()
        con = 0
        while con == 0:
            for rec in border_lis:
                for x in self.recs:
                    # 判断是否到底
                    next_x = [x[0], x[1] + 1, 30, 30]
                    if pygame.rect.Rect(next_x).colliderect(rec):
                        con = 1
            if con == 0:
                for x in self.recs:
                    x[1] += 1

    # 模拟瞬间下落
    def virtual_go_fast(self):
        my_lis = []
        for x in self.recs:
            if x[0] not in my_lis:
                my_lis.append(x[0])
        border_lis = []
        for rec in self.border_fixed_rec:
            if rec[0] in my_lis:
                border_lis.append(rec)
        border_lis.sort()
        con = 0
        virtual_recs = copy.deepcopy(self.recs)
        while con == 0:
            for rec in border_lis:
                for x in virtual_recs:
                    # 判断是否到底
                    next_x = [x[0], x[1] + 1, 30, 30]
                    if pygame.rect.Rect(next_x).colliderect(rec):
                        con = 1
                        for r in virtual_recs:
                            pygame.draw.rect(self.screen, [255, 100, 100], [r[0], r[1], 30, 30], 2)
                            pygame.draw.line(self.screen, [255, 100, 100], (r[0], r[1]), (r[0] + 30, r[1] + 30), 2)
                            pygame.draw.line(self.screen, [255, 100, 100], (r[0] + 30, r[1]), (r[0], r[1] + 30), 2)
            if con == 0:
                for x in virtual_recs:
                    x[1] += 1

    # 创建新块
    def create_new(self):
        # 随机选择
        self.now_box = self.next_box
        self.next_box = self.choice(random.randint(1, 7))
        # 创建矩形
        self.rec_1 = self.now_box.recs[0]
        self.rec_2 = self.now_box.recs[1]
        self.rec_3 = self.now_box.recs[2]
        self.rec_4 = self.now_box.recs[3]
        # 下一个
        rec_1 = self.next_box.recs[0]
        rec_2 = self.next_box.recs[1]
        rec_3 = self.next_box.recs[2]
        rec_4 = self.next_box.recs[3]
        self.recs = [self.rec_1, self.rec_2, self.rec_3, self.rec_4]
        self.rec_1_color = self.rec_1_next
        self.rec_2_color = self.rec_2_next
        self.rec_3_color = self.rec_3_next
        self.rec_4_color = self.rec_4_next
        if self.de_color == 0:
            c = [random.randint(10, 245), random.randint(10, 245), random.randint(10, 245)]
        else:
            c = self.de_color
        self.rec_1_next = c
        self.rec_2_next = c
        self.rec_3_next = c
        self.rec_4_next = c
        # 创建下一个块
        self.small_1 = [rec_1[0]+690, rec_1[1]+190, 30, 30]
        self.small_2 = [rec_2[0]+690, rec_2[1]+190, 30, 30]
        self.small_3 = [rec_3[0]+690, rec_3[1]+190, 30, 30]
        self.small_4 = [rec_4[0]+690, rec_4[1]+190, 30, 30]

    # 选择块
    def choice(self, number):
        if number == 1:
            return Trig()
        elif number == 2:
            return Beeline()
        elif number == 3:
            return LBeeline()
        elif number == 4:
            return RBeeline()
        elif number == 5:
            return Field()
        elif number == 6:
            return LLadder()
        elif number == 7:
            return RLadder()

    # 到达底部固定
    def fix(self):
        # 消除误差
        for rect in self.recs:
            rect[1] = (rect[1] // 30) * 30 + 8

        # 这四个块加入累计
        self.accumulate_list.append([self.rec_1, self.rec_1_color])
        self.accumulate_list.append([self.rec_2, self.rec_2_color])
        self.accumulate_list.append([self.rec_3, self.rec_3_color])
        self.accumulate_list.append([self.rec_4, self.rec_4_color])
        # 加入边界块
        for rec in self.recs:
            self.border_fixed_rec.append(rec)
        # 判断消除
        lis = [int(self.rec_1[1]), int(self.rec_2[1]), int(self.rec_3[1]), int(self.rec_4[1])]
        li = []
        for x in lis:
            if x not in li:
                li.append(x)
        li.reverse()
        self.eliminate(li)
        # 创建新块
        self.create_new()
        # 还原变形记录
        self.change_record = 0

    # 判断消除
    def eliminate(self, lis):
        for y in lis:
            count = 0
            for rec in self.accumulate_list:
                if int(rec[0][1]) == int(y):
                    count += 1
            if count == 15:
                # 清除累计
                template = []
                for rect in self.accumulate_list:
                    if int(rect[0][1]) != int(y):
                        template.append(rect)
                self.accumulate_list = template
                # 清除边界
                template = []
                for rect in self.border_fixed_rec:
                    if int(rect[1]) != int(y):
                        template.append(rect)
                self.border_fixed_rec = template
                # 加入下边界
                for x in range(21):
                    self.border_fixed_rec.append([681 + x * 30, 938, 30, 30])
                # 左右边界
                for c in range(33):
                    self.border_fixed_rec.append([651, 9 + c * 30, 30, 30])
                    self.border_fixed_rec.append([1282, 9 + c * 30, 30, 30])
                # 上面的下移
                for rect in self.accumulate_list:
                    if int(rect[0][1]) < int(y):
                        rect[0][1] += 30
                        if rect[0][1] % 30 == 7:
                            rect[0][1] += 1
                        elif rect[0][1] % 30 == 9:
                            rect[0][1] -= 1
                # 重新加入检查
                lis.append(y)
                # 得分加1
                self.my_count += 1

    # 画出块
    def draw_box(self):
        # 不画超出范围的部分
        if self.rec_1[1] >= 40:
            pygame.draw.rect(self.screen, self.rec_1_color, self.rec_1)
        elif self.rec_1[1] >= 10:
            pygame.draw.rect(self.screen, self.rec_1_color, [self.rec_1[0], 40, 30, abs(-self.rec_1[1] + 10)])
        if self.rec_2[1] >= 40:
            pygame.draw.rect(self.screen, self.rec_2_color, self.rec_2)
        elif self.rec_2[1] >= 10:
            pygame.draw.rect(self.screen, self.rec_2_color, [self.rec_2[0], 40, 30, abs(-self.rec_2[1] + 10)])
        if self.rec_3[1] >= 40:
            pygame.draw.rect(self.screen, self.rec_3_color, self.rec_3)
        elif self.rec_3[1] >= 10:
            pygame.draw.rect(self.screen, self.rec_3_color, [self.rec_3[0], 40, 30, abs(-self.rec_3[1] + 10)])
        if self.rec_4[1] >= 40:
            pygame.draw.rect(self.screen, self.rec_4_color, self.rec_4)
        elif self.rec_4[1] >= 10:
            pygame.draw.rect(self.screen, self.rec_4_color, [self.rec_4[0], 40, 30, abs(-self.rec_4[1] + 10)])

    # 显示界面
    def show_info(self):
        font = pygame.font.SysFont('simhei', 20, True, True)
        # 主框
        pygame.draw.rect(self.screen, (50, 10, 200), (680, 40, 454, 900), 3)
        # 显示下一个块的框
        self.screen.blit(self.box_picture, (1430, 70))
        # 显示得分
        text = self.my_font.render('得分 %d' % self.my_count, True, (50, 50, 250))
        self.screen.blit(text, (1530, 350))
        pygame.draw.lines(self.screen, (200, 250, 0), True, [(1510, 340), (1690, 340), (1690, 390), (1510, 390)], 4)
        pygame.draw.lines(self.screen, (self.lines_color1, 0, self.lines_color3), True, [(1510, 340), (1690, 340),
                                                                                         (1690, 390), (1510, 390)], 2)
        # 显示等级
        font1 = pygame.font.SysFont('songti', 50, True, True)
        text = font1.render(str(self.level), True, (200, 0, 200))
        self.screen.blit(text, (280, 190))
        text = font1.render('level', True, (200, 100, 0))
        self.screen.blit(text, (250, 110))
        pygame.draw.rect(self.screen, [0, 0, 0], [200, 150, 200, 100], 3)
        # 画出累计
        for rec in self.accumulate_list:
            pygame.draw.rect(self.screen, rec[1], rec[0])
        # 画出下一个
        pygame.draw.rect(self.screen, self.rec_1_next, self.small_1)
        pygame.draw.rect(self.screen, self.rec_2_next, self.small_2)
        pygame.draw.rect(self.screen, self.rec_3_next, self.small_3)
        pygame.draw.rect(self.screen, self.rec_4_next, self.small_4)
        # 重新开始选择框
        pygame.draw.rect(self.screen, (150, 10, 200), self.restart_box)
        pygame.draw.rect(self.screen, (0, 150, self.lines_color3), self.restart_box, 2)
        text = font.render('重新开始', True, (255, 255, 250))
        self.screen.blit(text, (1560, 466))
        # 暂停开始音乐框
        pygame.draw.rect(self.screen, (150, 0, 80), self.music_box)
        pygame.draw.rect(self.screen, (self.lines_color1, self.lines_color2, self.lines_color3), self.music_box, 2)
        if self.stop_music == 0:
            text = font.render('暂停音乐', True, (255, 255, 255))
        else:
            text = font.render('打开音乐', True, (255, 255, 255))
        self.screen.blit(text, (1555, 605))
        # 显示格子选择框
        pygame.draw.rect(self.screen, (50, 100, 150), self.show_lines_box)
        pygame.draw.rect(self.screen, (self.lines_color1, self.lines_color2, self.lines_color3), self.show_lines_box, 2)
        if self.show_lines == -1:
            text = font.render('显示格子', True, (255, 255, 255))
        else:
            text = font.render('隐藏格子', True, (255, 255, 255))
        self.screen.blit(text, (208, 355))
        # 暂停选择框
        pygame.draw.rect(self.screen, (50, 100, 150), self.pause_box)
        pygame.draw.rect(self.screen, (self.lines_color1, self.lines_color2, self.lines_color3), self.pause_box, 2)
        font = pygame.font.SysFont('simhei', 20, True, True)
        if self.pause == -1:
            text = font.render('暂停', True, (255, 255, 255))
        else:
            text = font.render('开始', True, (255, 255, 255))
        self.screen.blit(text, (208, 405))
        # 是否画出格子
        if self.show_lines == 1:
            for x in range(14):
                pygame.draw.line(self.screen, (self.lines_color1, self.lines_color2, self.lines_color3),
                                 (711 + 30*x, 40), (711 + 30*x, 940), 1)
            for y in range(29):
                pygame.draw.line(self.screen, (self.lines_color1, self.lines_color2, self.lines_color3), (681, 68+30*y),
                                 (1132, 68+30*y), 1)
        # 画出排行榜
        # 画出边框
        pygame.draw.lines(self.screen, (250, 20, 50), False, [(400, 450), (400, 500), (160, 500), (160, 550),
                                                              (400, 550), (400, 600), (160, 600), (160, 650)], 2)
        pygame.draw.line(self.screen, (250, 20, 50), (270, 450), (270, 650), 2)
        pygame.draw.lines(self.screen, (self.lines_color1, self.lines_color2, self.lines_color3), True,
                          [(160, 450), (400, 450), (400, 650), (160, 650)], 3)
        # 表头和分数
        font = pygame.font.SysFont('fangsong', 25, True, True)
        text = font.render('排名    分数', True, (190, 60, 80))
        self.screen.blit(text, (190, 460))
        text = font.render('第一     %d' % record_list[0], True, (190, 60, 80))
        self.screen.blit(text, (190, 510))
        text = font.render('第二     %d' % record_list[1], True, (190, 60, 80))
        self.screen.blit(text, (190, 560))
        text = font.render('第三     %d' % record_list[2], True, (190, 60, 80))
        self.screen.blit(text, (190, 610))
        if self.level < 15:
            self.level = self.my_count // 5 + 1
        # # 测试：画出边框矩形
        # for rec in self.border_fixed_rec:
        #     pygame.draw.rect(self.screen, (200, 0, 100), rec)

    # 判断Game Over
    def judge_end(self):
        for rec in self.accumulate_list:
            if rec[0][1] < 50:
                self.end = 1
                # 判断是否破纪录
                if self.my_count > record_list[0]:
                    record_list[0], record_list[1], record_list[2] = self.my_count, record_list[0], \
                                                                     record_list[1]
                elif self.my_count > record_list[1]:
                    record_list[1], record_list[2] = self.my_count, record_list[1]
                elif self.my_count > record_list[2]:
                    record_list[2] = self.my_count
                # 写入文件
                f = open('./record.txt', 'w')
                f.write(str(record_list))
                f.close()

    # 改变颜色
    def change_color(self):
        if self.mix_color == 1:
            # 实时改变格子颜色
            # R
            if self.lines_color3 == 255 and self.lines_color2 == 0:
                if self.lines_color1 < 255:
                    self.lines_color1 += 3
                else:
                    self.lines_color1 = 255
            elif self.lines_color3 == 0 and self.lines_color2 == 255:
                if self.lines_color1 > 0:
                    self.lines_color1 -= 3
                else:
                    self.lines_color1 = 0
            # G
            if self.lines_color1 == 255 and self.lines_color3 == 0:
                if self.lines_color2 < 255:
                    self.lines_color2 += 3
                else:
                    self.lines_color2 = 255
            elif self.lines_color1 == 0 and self.lines_color3 == 255:
                if self.lines_color2 > 0:
                    self.lines_color2 -= 3
                else:
                    self.lines_color2 = 0
            # B
            if self.lines_color1 == 0 and self.lines_color2 == 255:
                if self.lines_color3 < 255:
                    self.lines_color3 += 3
                else:
                    self.lines_color3 = 255
            elif self.lines_color1 == 255 and self.lines_color2 == 0:
                if self.lines_color3 > 0:
                    self.lines_color3 -= 3
                else:
                    self.lines_color3 = 0
        # 改变按钮颜色
        font = pygame.font.SysFont('simhei', 20, True, True)
        pos = pygame.mouse.get_pos()
        if self.restart_box.collidepoint(pos[0], pos[1]):
            text = font.render('重新开始', True, (255, 0, 0))
            self.screen.blit(text, (1560, 466))
        elif self.show_lines_box.collidepoint(pos[0], pos[1]):
            if self.show_lines == -1:
                text = font.render('显示格子', True, (0, 0, 255))
            else:
                text = font.render('隐藏格子', True, (0, 0, 255))
            self.screen.blit(text, (208, 355))
        elif self.pause_box.collidepoint(pos[0], pos[1]):
            if self.pause == -1:
                text = font.render('暂停', True, (0, 0, 255))
            else:
                text = font.render('开始', True, (0, 0, 255))
            self.screen.blit(text, (208, 405))
        elif self.music_box.collidepoint(pos[0], pos[1]):
            if self.stop_music == 0:
                text = font.render('暂停音乐', True, (0, 0, 255))
            else:
                text = font.render('打开音乐', True, (0, 0, 255))
            self.screen.blit(text, (1555, 605))

    # 主循环
    def began(self):
        while 1:
            self.time_record += 1
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_press = pygame.key.get_pressed()
                    # alt+f4退出
                    if key_press[K_LALT] and key_press[K_F4]:
                        pygame.display.quit()
                        exit()
                    # 移动变形
                    if self.pause == -1:
                        if key_press[K_LEFT]:
                            self.transverse(1)
                        if key_press[K_RIGHT]:
                            self.transverse(2)
                        if key_press[K_UP]:
                            self.change()
                        if key_press[K_DOWN]:
                            Thread(target=self.go_fast).start()
                            self.down_fast = 1
                    # RALT固定格子
                    if key_press[K_RALT]:
                        self.mix_color *= -1
                        if self.mix_color == -1:
                            [self.lines_color1, self.lines_color2, self.lines_color3] = [0, 0, 0]
                elif event.type == MOUSEBUTTONDOWN:
                    bd = pygame.mouse.get_pressed()
                    if bd[0] == 1:
                        pos = pygame.mouse.get_pos()
                        # 左键单击重新开始
                        if self.restart_box.collidepoint(pos[0], pos[1]):
                            # 判断是否破纪录
                            if self.my_count > record_list[0]:
                                record_list[0], record_list[1], record_list[2] = self.my_count, record_list[0], \
                                                                                 record_list[1]
                            elif self.my_count > record_list[1]:
                                record_list[1], record_list[2] = self.my_count, record_list[1]
                            elif self.my_count > record_list[2]:
                                record_list[2] = self.my_count
                            # 写入文件
                            f = open('./record.txt', 'w')
                            f.write(str(record_list))
                            f.close()
                            self.__init__()
                            continue
                        # 左键单击显示/隐藏格子
                        elif self.show_lines_box.collidepoint(pos[0], pos[1]):
                            self.show_lines *= -1
                        # 左键单击暂停
                        elif self.pause_box.collidepoint(pos[0], pos[1]):
                            self.pause *= -1
                        # 左键单击打开暂停BGM
                        elif self.music_box.collidepoint(pos[0], pos[1]):
                            if self.stop_music == 0:
                                pygame.mixer_music.pause()
                                self.stop_music = 1
                            else:
                                pygame.mixer_music.unpause()
                                self.stop_music = 0
            self.screen.blit(self.bg_picture, (0, 0))
            # 下落
            if self.pause == -1:
                self.move_down()
            # 显示
            self.show_info()
            self.draw_box()
            self.virtual_go_fast()
            # 实时改变按钮颜色
            self.change_color()
            # 判断结束
            if self.end == 0:
                self.judge_end()
            if 0 < self.end < 3:
                # 显示Game Over
                text = self.my_font.render('Game Over!', True, (255, 50, 100))
                self.screen.blit(text, (850, 450))
                text = self.my_font.render('最终得分 %d' % self.my_count, True, (255, 50, 100))
                self.screen.blit(text, (840, 550))
                self.end += 1
            if self.end != 3:
                pygame.display.update()


# 各种块的初始坐标
class Trig(object):
    def __init__(self):
        self.recs = [
            [892, -22, 30, 30],
            [892, 8, 30, 30],
            [862, 8, 30, 30],
            [922, 8, 30, 30],
        ]


class Beeline(object):
    def __init__(self):
        self.recs = [
            [892, -82, 30, 30],
            [892, -52, 30, 30],
            [892, -22, 30, 30],
            [892, 8, 30, 30],
        ]


class LBeeline(object):
    def __init__(self):
        self.recs = [
            [862, -22, 30, 30],
            [892, 8, 30, 30],
            [862, 8, 30, 30],
            [922, 8, 30, 30],
        ]


class RBeeline(object):
    def __init__(self):
        self.recs = [
            [922, -22, 30, 30],
            [892, 8, 30, 30],
            [862, 8, 30, 30],
            [922, 8, 30, 30],
        ]


class Field(object):
    def __init__(self):
        self.recs = [
            [862, -22, 30, 30],
            [862, 8, 30, 30],
            [892, -22, 30, 30],
            [892, 8, 30, 30],
        ]


class LLadder(object):
    def __init__(self):
        self.recs = [
            [892, -22, 30, 30],
            [892, 8, 30, 30],
            [862, -22, 30, 30],
            [922, 8, 30, 30],
        ]


class RLadder(object):
    def __init__(self):
        self.recs = [
            [892, -22, 30, 30],
            [892, 8, 30, 30],
            [862, 8, 30, 30],
            [922, -22, 30, 30],
        ]


russia = Russia()
russia.began()
