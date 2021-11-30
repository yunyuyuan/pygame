import os, re, time, win32api
import pygame
from pygame.locals import *
from sys import exit
pygame.init()
disk = 'disk.png'
direct = 'dir.png'
file_ = 'file.png'
back = 'back.png'
back_red = 'back_red.png'


# 找到存在的磁盘
def find_disk():
    lis = []
    for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
        try:
            os.listdir(i + '://')
            lis.append(i)
        except FileNotFoundError:
            pass
    return lis


class Browser(object):
    def __init__(self):
        self.screen = pygame.display.set_mode([1200, 900], 0, 32)
        pygame.display.set_caption('文件管理器')
        # 图片
        self.disk_pic = pygame.image.load(disk).convert_alpha()
        self.dir_pic = pygame.image.load(direct).convert_alpha()
        self.file_pic = pygame.image.load(file_).convert_alpha()
        self.back_pic = pygame.image.load(back).convert_alpha()
        self.back_red_pic = pygame.image.load(back_red).convert_alpha()
        # 字体
        self.font = pygame.font.SysFont('fangsong', 20, True)
        self.font1 = pygame.font.SysFont('kaiti', 20, False)
        # 初始项
        self.show_what = 0
        self.now_dir = 'C://'
        self.pos = [0, 0]
        # 磁盘
        self.disk_lis = find_disk()
        self.dir_lis = []
        self.scroll = 0

    # 显示磁盘
    def show_disk(self):
        t = 0
        for i in self.disk_lis:
            self.screen.blit(self.disk_pic, [t * 100 + 100, 100])
            text = self.font.render(i, True, [0, 200, 100])
            self.screen.blit(text, [t * 100 + 172, 220])
            t += 1

    # 显示目录
    def show_dir(self):
        # 显示框架
        pygame.draw.rect(self.screen, [0, 0, 0], [157, 70, 900, 655], 3)
        if len(self.dir_lis) > 25:
            pass
        self.dir_lis = os.listdir(self.now_dir)
        show_lis = self.dir_lis[self.scroll:][0:25]
        # 显示路径
        pygame.draw.rect(self.screen, [0, 200, 30], [240, 25, 600, 30], 2)
        if len(self.now_dir) < 55:
            text = self.font1.render(self.now_dir, True, [50, 30, 50])
        else:
            text = self.font1.render(self.now_dir[:55] + '...', True, [50, 30, 50])
        self.screen.blit(text, [250, 30])
        # 顶层列名称
        text = self.font1.render(
            '名称                          创建日期                  类型         大小(子目录)', True, [50, 50, 50])
        self.screen.blit(text, [200, 75])
        # 显示文件夹图标
        t = 0
        for i in show_lis:
            d = self.now_dir + '/' + i
            if re.search('///', d):
                d = re.sub('///', '//', d)
            # 是文件夹
            if os.path.isdir(d):
                self.screen.blit(self.dir_pic, [170, t * 25 + 100])
            # 是文件
            else:
                self.screen.blit(self.file_pic, [170, t * 25 + 100])
            t += 1
        # 显示文件信息
        t = 0
        for i in show_lis:
            d = self.now_dir + '/' + i
            # 名字
            if len(i) > 23:
                m = i[0:23] + '...'
            else:
                m = i
            text = self.font1.render(m, True, [0, 0, 0])
            self.screen.blit(text, [200, t * 25 + 100])
            # 创建日期
            text = self.font1.render(time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(d))), True, [0, 0, 0])
            self.screen.blit(text, [500, t * 25 + 100])
            # 类型
            if not os.path.isdir(d):
                text = self.font1.render(
                    os.path.splitext(d)[1][1:], True, [0, 0, 0])
            else:
                text = self.font1.render(
                    '文件夹', True, [0, 0, 0])
            self.screen.blit(text, [760, t * 25 + 100])
            # 大小
            if not os.path.isdir(d):
                size = os.path.getsize(d)
                if 1073741824 <= size < 1099511627776:
                    size = str(round(size/1073741824)) + 'G'
                elif 1048576 <= size < 1073741824:
                    size = str(round(size/1048576)) + 'M'
                elif 1024 <= size < 1048576:
                    size = str(round(size/1204)) + 'K'
                elif size < 1024:
                    size = str(round(size)) + 'B'
                text = self.font1.render(
                    size, True, [0, 0, 0])
                self.screen.blit(text, [900, t * 25 + 100])
            else:
                try:
                    text = self.font1.render(str(len(os.listdir(d))) + '个', True, [0, 0, 0])
                except PermissionError:
                    text = self.font1.render('无法访问', True, [250, 100, 0])
                self.screen.blit(text, [900, t * 25 + 100])
            t += 1
        # 显示返回按钮
        self.screen.blit(self.back_pic, [20, 30])

    # 更改颜色
    def change_color(self):
        pos = pygame.mouse.get_pos()
        # 磁盘区
        if self.show_what == 0:
            t = 0
            for i in self.disk_lis:
                if (t * 100 + 150) < pos[0] < (t * 100 + 215) and 130 < pos[1] < 210:
                    text = self.font.render(i, True, [200, 2, 100])
                    self.screen.blit(text, [t * 100 + 172, 220])
                t += 1
        # 目录区
        elif self.show_what == 1:
            # 返回按键
            if ((pos[0] - 53)**2 + (pos[1] - 70)**2)**0.5 < 40:
                self.screen.blit(self.back_red_pic, [20, 30])
            # 文件
            if 155 < pos[0] < 1011 and 100 < pos[1] < len(self.dir_lis)*25 + 100:
                pygame.draw.rect(self.screen, [150, 150, 0], [160, ((pos[1]-100) // 25) * 25 + 100, 850, 23], 2)

    # 点击事件
    def do_something(self):
        # 磁盘区
        if self.show_what == 0:
            t = 0
            for i in self.disk_lis:
                if (t * 100 + 150) < self.pos[0] < (t * 100 + 215) and 130 < self.pos[1] < 210:
                    self.show_what = 1
                    self.now_dir = i + '://'
                    return
                t += 1
        # 目录区
        elif self.show_what == 1:
            # 返回按键
            if ((self.pos[0] - 53) ** 2 + (self.pos[1] - 70) ** 2) ** 0.5 < 40:
                print(self.now_dir)
                # 次级目录
                if re.match('.://.', self.now_dir):
                    self.now_dir = re.search('(.*)/.*?', self.now_dir).group(1)
                # 顶级目录
                else:
                    self.show_what = 0
                self.scroll = 0
            # 点击文件或文件
            if 155 < self.pos[0] < 1011 and 100 < self.pos[1] < len(self.dir_lis) * 25 + 100:
                # 点击文件夹
                ind = (self.pos[1] - 100) // 25
                d = self.now_dir + '/' + self.dir_lis[ind]
                if os.path.isdir(d):
                    try:
                        os.listdir(d)
                        self.now_dir = d
                    except PermissionError:
                        print('拒绝访问')
                    if re.search('///', self.now_dir):
                        self.now_dir = re.sub('///', '//', self.now_dir)
                else:
                    # 点击文件
                    try:
                        win32api.ShellExecute(0, 'open', d, '', '', 1)
                    except:
                        pass

    def start(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.pos = pygame.mouse.get_pos()
                        self.do_something()
                    # 滚轮朝上
                    elif event.button == 4 and len(self.dir_lis) >= 25:
                        if 155 < self.pos[0] < 1011 and 100 < self.pos[1] < len(self.dir_lis) * 25 + 100\
                                and self.show_what == 1 and self.scroll >= 2:
                            self.scroll -= 2
                    # 滚轮朝下
                    elif event.button == 5 and len(self.dir_lis) >= 25:
                        if 155 < self.pos[0] < 1011 and 100 < self.pos[1] < len(self.dir_lis) * 25 + 100 \
                                and self.show_what == 1 and len(self.dir_lis[self.scroll:]) > 27:
                            self.scroll += 2
            self.screen.fill([205, 200, 200])
            if self.show_what == 0:
                self.show_disk()
            elif self.show_what == 1:
                self.show_dir()
            self.change_color()
            pygame.display.update()


b = Browser()
b.start()

