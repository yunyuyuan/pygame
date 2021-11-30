import pygame, math, copy
from pygame.locals import *
from sys import exit
from 小工具.Rainbow import rainbow
from 小工具.time_record import Timer

# 背景
bg = './bg.jpg'
# 菜单相关
menu = './menu/menu.png'
continue_ = './menu/continue.png'
choose = './menu/choose.png'
set_ = './menu/set.png'
rate = './menu/rate.png'
exit_ = './menu/exit.png'
about = './menu/about.png'
# 选择关卡相关
hard = './choose/hard.png'
item = './choose/item.png'
finish = './choose/finish.png'
select = './choose/select.png'
next_ = './back/next.png'
next_red = './back/next_red.png'
before_red = './back/before_red.png'
before = './back/before.png'
# 排行榜
record = './box/record.png'
# 关于
about_ = './box/about.png'
# 返回按钮
back = './back/back.png'
red_back = './back/back_red.png'
# 保存按钮
save = './save/save.png'
save_red = './save/save_red.png'
# 重置按钮
refresh = './save/refresh.png'
refresh_red = './save/refresh_red.png'
# 数据
data = './data/data.txt'
continue_game = './data/continue_game.txt'
about_text = './data/about.txt'
# 游戏记录数据
game_record = './data/record.txt'
# 时间框
time_record = './box/time.png'
# 半透明框
transparent = './box/transparent.png'
pygame.init()


class ShuDu(object):
    def __init__(self):
        # 初始化屏幕和图片
        self.screen = pygame.display.set_mode([1920, 1080], FULLSCREEN, 32)
        # 背景
        self.bg_picture = pygame.image.load(bg).convert()
        # 菜单项
        self.menu_picture = pygame.image.load(menu).convert_alpha()
        self.menu_continue_picture = pygame.image.load(continue_).convert_alpha()
        self.menu_choose_picture = pygame.image.load(choose).convert_alpha()
        self.menu_set_picture = pygame.image.load(set_).convert_alpha()
        self.menu_rate_picture = pygame.image.load(rate).convert_alpha()
        self.menu_about_picture = pygame.image.load(about).convert_alpha()
        self.menu_exit_picture = pygame.image.load(exit_).convert_alpha()
        # 选择关卡相关
        self.hard_picture = pygame.image.load(hard).convert_alpha()
        self.item_picture = pygame.image.load(item).convert_alpha()
        self.finish_picture = pygame.image.load(finish).convert_alpha()
        self.select_picture = pygame.image.load(select).convert_alpha()
        self.next = pygame.image.load(next_).convert_alpha()
        self.next_red = pygame.image.load(next_red).convert_alpha()
        self.before = pygame.image.load(before).convert_alpha()
        self.before_red = pygame.image.load(before_red).convert_alpha()
        # 排行榜相关
        self.record_picture = pygame.image.load(record).convert_alpha()
        # 关于相关
        self.about_picture = pygame.image.load(about_).convert_alpha()
        # 游戏界面
        self.transparent = pygame.image.load(transparent).convert_alpha()
        # 返回按钮
        self.back_picture = pygame.image.load(back).convert_alpha()
        self.red_back_picture = pygame.image.load(red_back).convert_alpha()
        # 保存按钮
        self.save_picture = pygame.image.load(save).convert_alpha()
        self.save_red_picture = pygame.image.load(save_red).convert_alpha()
        # 重置按钮
        self.refresh_picture = pygame.image.load(refresh).convert_alpha()
        self.refresh_red_picture = pygame.image.load(refresh_red).convert_alpha()
        # 时间框
        self.time_picture = pygame.image.load(time_record).convert_alpha()
        # 显示状况
        self.condition = 0
        # 字体
        self.font = pygame.font.SysFont('kaiti', 40, True, True)
        self.font1 = pygame.font.SysFont('fangsong', 28, True, True)
        self.font2 = pygame.font.SysFont('microsoftyahei', 50, False, True)
        # 当前难度相关
        self.hard_lis = ['简单', '中等', '困难', '自定义']
        self.what_hard = 0
        # 读取关卡数据
        f = open(data, 'r')
        s = f.read()
        self.how_item = eval(s)
        f.close()
        # 正在运行的游戏,具体到行
        self.going_kind = self.hard_lis[self.what_hard]
        self.going_line = 0
        # 选定的格子
        self.selected_block = [-1, -1]
        # 自定义数独时选定格子
        self.set_game_selected = [-1, -1]
        # 游戏缓存
        self.game = [[[0, 0] for x in range(9)] for x in range(9)]
        self.copy_game = [[[0, 0] for x in range(9)] for x in range(9)]
        # 自定义中的游戏
        self.setting_game = [[[0, 0] for x in range(9)] for x in range(9)]
        # 是否出错
        self.mistake = 0
        # 颜色
        self.color = [255, 0, 0]
        self.color1 = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255)]
        # 进行时间
        self.time_record = 0
        # 获胜
        self.win = 0
        self.judge = 0
        # 用完的数字
        self.used = [0 for x in range(9)]

    # 游戏菜单
    def game_menu(self):
        while 1:
            # 获取鼠标位置
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_press = pygame.key.get_pressed()
                    if key_press[K_LALT] and key_press[K_F4]:
                        pygame.display.quit()
                        exit()
                    # 自定义界面
                    if self.condition == 3:
                        if event.key in range(257, 267) and self.set_game_selected != [-1, -1]:
                            if event.key in range(257, 266):
                                num = event.key - 257
                                # 替换数字
                                self.setting_game[self.set_game_selected[1]][self.set_game_selected[0]][0] = num + 1
                                self.setting_game[self.set_game_selected[1]][self.set_game_selected[0]][1] = 1
                            # 点击退格删除数字(填入0)
                            else:
                                self.setting_game[self.set_game_selected[1]][self.set_game_selected[0]][0] = 0
                                self.setting_game[self.set_game_selected[1]][self.set_game_selected[0]][1] = 0
                        elif event.key == 273 and self.set_game_selected[1] > 0:
                            self.set_game_selected[1] -= 1
                        elif event.key == 274 and self.set_game_selected[1] < 8:
                            self.set_game_selected[1] += 1
                        elif event.key == 275 and self.set_game_selected[0] < 8:
                            self.set_game_selected[0] += 1
                        elif event.key == 276 and self.set_game_selected[0] > 0:
                            self.set_game_selected[0] -= 1
                elif event.type == MOUSEBUTTONDOWN:
                    what_press = pygame.mouse.get_pressed()
                    # 左键点击
                    if what_press == (1, 0, 0):
                        self.do_something(mouse_pos)
                    # 右键删除
                    if what_press == (0, 0, 1):
                        pass
            # 画背景
            self.screen.blit(self.bg_picture, [0, 0])
            # 根据不同状况显示菜单项
            # 主菜单
            if self.condition == 0:
                self.screen.blit(self.menu_picture, [850, 350])
            # 选择关卡
            if self.condition == 1:
                self.choose_level()
            # 排行榜
            if self.condition == 2:
                self.record()
            # 自定义
            if self.condition == 3:
                self.set_own()
            # 关于
            if self.condition == 4:
                self.about()
            # 动态改变按钮颜色
            self.change_color(mouse_pos)
            pygame.display.update()

    # 找出游戏
    def find_game(self):
        f = open('./data/%s/%d.txt' % (self.going_kind, self.going_line), 'r')
        s = f.read()
        f.close()
        return eval(s)

    # 选择关卡项
    def choose_level(self):
        self.screen.blit(self.hard_picture, [800, 100])
        text = self.font.render(self.hard_lis[self.what_hard], True, [0, 0, 0])
        self.screen.blit(text, [890, 125])
        # 难度
        if self.how_item[self.what_hard][0] > 0:
            for x in range(self.how_item[self.what_hard][0]):
                self.screen.blit(self.item_picture, [(x % 10) * 100 + 440, (x // 10) * 150 + 300])
        mark = 0
        # 关卡
        try:
            for x in self.how_item[self.what_hard][1]:
                if x[0] != 0:
                    self.screen.blit(self.finish_picture, [(mark % 10) * 100 + 439, (mark // 10) * 150 + 300])
                mark += 1
                text = self.font2.render(str(mark), True, [50, 50, 0])
                self.screen.blit(text, [((mark - 1) % 10) * 100 + 464, ((mark - 1) // 10) * 150 + 380])
        except IndexError:
            pass
        self.screen.blit(self.back_picture, [100, 50])
        # 有上一个
        if self.what_hard != 0:
            self.screen.blit(self.before, [730, 114])
        # 有下一个
        if self.what_hard != 3:
            self.screen.blit(self.next, [1088, 110])

    # 数据榜
    def record(self):
        # 数据模板
        self.screen.blit(self.record_picture, [750, 200])
        # 返回按钮
        self.screen.blit(self.back_picture, [100, 50])
        # 重置按钮
        self.screen.blit(self.refresh_picture, [1575, 650])
        # 读取数据
        f = open(game_record, 'r')
        info = f.readlines()
        f.close()
        f = open(data, 'r')
        s = eval(f.read())
        t = []
        for x in s[0][1]:
            if x[0] != 0:
                t.append(x[0])
        info[0] = "['最快(简单)',%d]" % sorted(t)[0]
        t = []
        for x in s[1][1]:
            if x[0] != 0:
                t.append(x[0])
        info[1] = "['最快(中等)',%d]" % sorted(t)[0]
        t = []
        for x in s[2][1]:
            if x[0] != 0:
                t.append(x[0])
        info[2] = "['最快(困难)',%d]" % sorted(t)[0]
        t = 0
        for i in s:
            for x in i[1]:
                if x[0] != 0:
                    t += 1
        info[4] = "['完成局数',%d]" % t
        info[5] = "['完成百分比','%s']" % (str('%.3f' % (t/(s[0][0] + s[1][0] + s[2][0] + s[3][0]))) + '%')
        mark = 1
        for line in info:
            i = eval(line.strip())
            text = self.font1.render(i[0], True, [0, 0, 0])
            self.screen.blit(text, [830, mark * 89 + 120])
            if mark == 4:
                text = self.font1.render('%s:%s' % (i[1] // 60, i[1] % 60), True, [250, 100, 100])
            else:
                text = self.font1.render(str(i[1]), True, [250, 100, 100])
            self.screen.blit(text, [1050, mark * 89 + 120])
            mark += 1

    # 自定义
    def set_own(self):
        # 返回按钮
        self.screen.blit(self.back_picture, [100, 50])
        # 保存按钮
        self.screen.blit(self.save_picture, [1600, 500])
        # 重置按钮
        self.screen.blit(self.refresh_picture, [1575, 650])
        # 画游戏框界面
        for x in range(10):
            pygame.draw.line(self.screen, [0, 0, 0], [x * 90 + 500, 150], [x * 90 + 500, 825], 2)
            pygame.draw.line(self.screen, [0, 0, 0], [500, x * 75 + 150], [1310, x * 75 + 150], 2)
        for x in range(4):
            pygame.draw.line(self.screen, [0, 0, 0], [x * 270 + 500, 150], [x * 270 + 500, 825], 5)
            pygame.draw.line(self.screen, [0, 0, 0], [500, x * 225 + 150], [1310, x * 225 + 150], 5)
        # 画出游戏数字
        temp = 0
        for line in self.setting_game:
            mark = 0
            for num in line:
                # 画出阴影
                if num[1] == 1:
                    self.screen.blit(self.transparent, [mark * 90 + 502, temp * 75 + 150])
                # 画出数字
                if num[0] != 0:
                    if self.judge_mistake(num[0], [mark, temp], self.setting_game):
                        c = [0, 0, 0]
                    else:
                        c = [255, 0, 0]
                    text = self.font2.render(str(num[0]), True, c)
                    self.screen.blit(text, [mark * 90 + 530, temp * 75 + 176])
                mark += 1
            temp += 1
        # 画出数字区
        for x in range(10):
            for y in self.color1:
                self.color1[self.color1.index(y)] = rainbow(y, 0.1)
            pygame.draw.rect(self.screen, self.color1[x], [x * 90 + 450, 900, 90, 90])
            if x < 9:
                text = self.font2.render(str(x + 1), True, [0, 0, 0])
                self.screen.blit(text, [x * 90 + 480, 930])
        # 退格
        text = self.font2.render('C', True, [0, 0, 0])
        self.screen.blit(text, [1290, 930])

    # 关于
    def about(self):
        f = open(about_text, 'r')
        info_lis = f.readlines()
        f.close()
        self.screen.blit(self.about_picture, [430, 150])
        mark = 1
        for info in info_lis:
            info = eval(info)
            text = self.font2.render(str(info[0]), True, [50, 200, 50])
            self.screen.blit(text, [700, mark * 100 + 250])
            text = self.font2.render(str(info[1]), True, [255, 20, 50])
            self.screen.blit(text, [1000, mark * 100 + 250])
            mark += 1
        self.screen.blit(self.back_picture, [100, 50])

    # 不同菜单项的点击事件
    def do_something(self, pos):
        # 在主菜单界面
        if self.condition == 0:
            # 继续游戏
            if 850 < pos[0] < 1065 and 350 < pos[1] < 410:
                # 载入存档并开始游戏
                f = open(continue_game, 'r')
                info = eval(f.read())
                self.going_kind = info[0]
                self.going_line = info[1]
                self.condition = 5
                # 读取初始时间
                self.time_record = self.how_item[self.what_hard][1][info[1]][1]
                self.began()
            # 选择关卡
            if 850 < pos[0] < 1065 and 445 < pos[1] < 505:
                self.condition = 1
            # 排行榜
            if 850 < pos[0] < 1065 and 540 < pos[1] < 600:
                self.condition = 2
            # 自定义
            if 850 < pos[0] < 1065 and 630 < pos[1] < 690:
                self.condition = 3
            # 关于
            if 850 < pos[0] < 1065 and 725 < pos[1] < 785:
                self.condition = 4
            # 退出游戏
            if 850 < pos[0] < 1065 and 820 < pos[1] < 880:
                pygame.display.quit()
                exit()
        # 在选择关卡界面
        elif self.condition == 1:
            # 返回主页面
            if math.sqrt((pos[0] - 138)**2 + (pos[1] - 89)**2) < 38:
                self.condition = 0
            # 开始游戏
            for x in range(self.how_item[self.what_hard][0]):
                if math.sqrt((pos[0] - ((x % 10) * 100 + 481))**2 + (pos[1] - ((x // 10) * 150 + 338))**2) < 35:
                    self.going_kind = self.hard_lis[self.what_hard]
                    self.going_line = x
                    self.condition = 5
                    # 读取初始时间
                    self.time_record = self.how_item[self.what_hard][1][x][1]
                    self.began()
            # 调节难度
            # 有上一个
            if self.what_hard != 0 and math.sqrt((pos[0] - 761) ** 2 + (pos[1] - 144) ** 2) < 30:
                self.what_hard -= 1
            # 有下一个
            if self.what_hard != 3 and math.sqrt((pos[0] - 1119) ** 2 + (pos[1] - 144) ** 2) < 30:
                self.what_hard += 1
        # 在排行榜界面
        elif self.condition == 2:
            # 返回
            if math.sqrt((pos[0] - 138)**2 + (pos[1] - 89)**2) < 38:
                self.condition = 0
            # 重置
            if math.sqrt((pos[0] - 1640) ** 2 + (pos[1] - 698) ** 2) < 44:
                f = open(game_record, 'w')
                f.write("['最快(简单)']\n['最快(中等)']\n['最快(困难)']\n['游戏总时间',0]\n['完成局数',0]\n['完成百分比',0]\n['好运指数',100]\n['挂科概率','0%']")
                f.close()
        # 在自定义界面
        elif self.condition == 3:
            # 返回
            if math.sqrt((pos[0] - 138)**2 + (pos[1] - 89)**2) < 38:
                self.condition = 0
                # 刷新关卡数据
                f = open(data, 'r')
                s = f.read()
                self.how_item = eval(s)
            # 点击保存按钮(不保存空的)
            if math.sqrt((pos[0] - 1640) ** 2 + (pos[1] - 540) ** 2) < 38 and self.setting_game != [[[0, 0] for x in range(9)] for x in range(9)]:
                # 获得已定义的游戏数
                num = self.how_item[3][0]
                self.how_item[3][0] = num + 1
                self.how_item[3][1].append([0, 0])
                # 保存到data
                f = open(data, 'w')
                f.write(str(self.how_item))
                f.close()
                # 保存到游戏文件夹
                f = open('./data/自定义/%d.txt' % num, 'w')
                f.write(str(self.setting_game))
                f.close()
            # 点击重置按钮
            if math.sqrt((pos[0] - 1640) ** 2 + (pos[1] - 698) ** 2) < 44:
                self.setting_game = [[[0, 0] for x in range(9)] for x in range(9)]
            # 点击格子区
            if 500 < pos[0] < 1310 and 150 < pos[1] < 825:
                # 设置格子行列
                draw_pos0 = (pos[0] - 500) // 90
                draw_pos1 = (pos[1] - 150) // 75
                self.set_game_selected = [draw_pos0, draw_pos1]
            # 当选定格子时,填入数字
            if self.set_game_selected != [-1, -1]:
                # 点击数字区填入数字
                if 450 < pos[0] < 1260 and 900 < pos[1] < 990:
                    num = (pos[0] - 450) // 90
                    print(num)
                    # 替换数字
                    self.setting_game[self.set_game_selected[1]][self.set_game_selected[0]][0] = num + 1
                    self.setting_game[self.set_game_selected[1]][self.set_game_selected[0]][1] = 1
                # 点击退格删除数字(填入0)
                elif 1260 < pos[0] < 1390:
                    self.setting_game[self.set_game_selected[1]][self.set_game_selected[0]][0] = 0
                    self.setting_game[self.set_game_selected[1]][self.set_game_selected[0]][1] = 0

        # 在关于界面
        elif self.condition == 4:
            if math.sqrt((pos[0] - 138)**2 + (pos[1] - 89)**2) < 38:
                self.condition = 0

    # 动态改变选项颜色
    def change_color(self, pos):
        # 主菜单页面
        if self.condition == 0:
            if 850 < pos[0] < 1065 and 350 < pos[1] < 410:
                self.screen.blit(self.menu_continue_picture, [887, 361])
            if 850 < pos[0] < 1065 and 445 < pos[1] < 505:
                self.screen.blit(self.menu_choose_picture, [882, 452])
            if 850 < pos[0] < 1065 and 540 < pos[1] < 600:
                self.screen.blit(self.menu_rate_picture, [912, 539])
            if 850 < pos[0] < 1065 and 630 < pos[1] < 690:
                self.screen.blit(self.menu_set_picture, [865, 641])
            if 850 < pos[0] < 1065 and 725 < pos[1] < 785:
                self.screen.blit(self.menu_about_picture, [916, 735])
            if 850 < pos[0] < 1065 and 820 < pos[1] < 880:
                self.screen.blit(self.menu_exit_picture, [921, 831])
        # 选择关卡页面
        elif self.condition == 1:
            # 关卡
            for x in range(self.how_item[self.what_hard][0]):
                if math.sqrt((pos[0] - ((x % 10) * 100 + 481))**2 + (pos[1] - ((x // 10) * 150 + 338))**2) < 35:
                    self.screen.blit(self.select_picture, [(x % 10) * 100 + 440, (x // 10) * 150 + 300])
                    # 最好完成时间
                    if self.how_item[self.what_hard][1][x][0] != 0:
                        text = self.font.render('最佳[%s:%s]' % (self.how_item[self.what_hard][1][x][0] // 60, self.how_item[self.what_hard][1][x][0] % 60), True, [255, 0, 200])
                        self.screen.blit(text, [605, 220])
                    # 进行时间
                    text = self.font.render('进行到[%s:%s]' % (
                    self.how_item[self.what_hard][1][x][1] // 60, self.how_item[self.what_hard][1][x][1] % 60), True,
                                            [0, 0, 0])
                    self.screen.blit(text, [925, 220])
            # 返回
            if math.sqrt((pos[0] - 138)**2 + (pos[1] - 89)**2) < 38:
                self.screen.blit(self.red_back_picture, [100, 50])
            # 有上一个
            if self.what_hard != 0 and math.sqrt((pos[0] - 761) ** 2 + (pos[1] - 144) ** 2) < 30:
                    self.screen.blit(self.before_red, [750, 127])
            # 有下一个
            if self.what_hard != 3 and math.sqrt((pos[0] - 1119)**2 + (pos[1] - 144)**2) < 30:
                self.screen.blit(self.next_red, [1106, 129])
        # 排行榜界面
        elif self.condition == 2:
            # 返回
            if math.sqrt((pos[0] - 138)**2 + (pos[1] - 89)**2) < 38:
                self.screen.blit(self.red_back_picture, [100, 50])
            # 重置
            if math.sqrt((pos[0] - 1640) ** 2 + (pos[1] - 698) ** 2) < 44:
                self.screen.blit(self.refresh_red_picture, [1575, 650])
        # 自定义页面
        elif self.condition == 3:
            self.color = rainbow(self.color, 1)
            # 返回
            if math.sqrt((pos[0] - 138) ** 2 + (pos[1] - 89) ** 2) < 38:
                self.screen.blit(self.red_back_picture, [100, 50])
            # 保存按钮
            if math.sqrt((pos[0] - 1640) ** 2 + (pos[1] - 540) ** 2) < 38:
                self.screen.blit(self.save_red_picture, [1621, 525])
            # 重置按钮
            if math.sqrt((pos[0] - 1640) ** 2 + (pos[1] - 698) ** 2) < 44:
                self.screen.blit(self.refresh_red_picture, [1575, 650])
            # 显示选定的格子
            if self.set_game_selected != [-1, -1]:
                pygame.draw.rect(self.screen, self.color,
                                 [self.set_game_selected[0] * 90 + 500, self.set_game_selected[1] * 75 + 150, 90, 75], 4)
        # 关于页面
        elif self.condition == 4:
            if math.sqrt((pos[0] - 138) ** 2 + (pos[1] - 89) ** 2) < 38:
                self.screen.blit(self.red_back_picture, [100, 50])

    # 开始游戏
    def began(self):
        # 寻找游戏
        self.game = self.find_game()
        self.copy_game = copy.deepcopy(self.game)
        timer = Timer()
        timer.began()
        while self.condition == 5:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # 退出
                    key_press = pygame.key.get_pressed()
                    if key_press[K_LALT] and key_press[K_F4]:
                        pygame.display.quit()
                        exit()
                    elif event.key in range(257, 267) and self.selected_block != [-1, -1] and self.win == 0:
                        if event.key in range(257, 266):
                            num = event.key - 257
                            if self.used[num] == 0:
                                # 替换数字
                                self.copy_game[self.selected_block[1]][self.selected_block[0]][0] = num + 1
                        # 点击退格删除数字(填入0)
                        else:
                            self.copy_game[self.selected_block[1]][self.selected_block[0]][0] = 0
                            self.mistake = 0
                        self.judge = 1
                    elif event.key == 273 and self.selected_block[1] > 0:
                        t = copy.deepcopy(self.selected_block)
                        while self.selected_block[1] > -1:
                            self.selected_block[1] -= 1
                            try:
                                if self.copy_game[self.selected_block[1]][self.selected_block[0]][1] != 1:
                                    break
                            except IndexError:
                                break
                        if self.selected_block[1] == -1:
                            self.selected_block = t
                    elif event.key == 274 and self.selected_block[1] < 8:
                        t = copy.deepcopy(self.selected_block)
                        while self.selected_block[1] < 9:
                            self.selected_block[1] += 1
                            try:
                                if self.copy_game[self.selected_block[1]][self.selected_block[0]][1] != 1:
                                    break
                            except IndexError:
                                break
                        if self.selected_block[1] == 9:
                            self.selected_block = t
                    elif event.key == 275 and self.selected_block[0] < 8:
                        t = copy.deepcopy(self.selected_block)
                        while self.selected_block[0] < 9:
                            self.selected_block[0] += 1
                            try:
                                if self.copy_game[self.selected_block[1]][self.selected_block[0]][1] != 1:
                                    break
                            except IndexError:
                                break
                        if self.selected_block[0] == 9:
                            self.selected_block = t
                    elif event.key == 276 and self.selected_block[0] > 0:
                        t = copy.deepcopy(self.selected_block)
                        while self.selected_block[0] > -1:
                            self.selected_block[0] -= 1
                            try:
                                if self.copy_game[self.selected_block[1]][self.selected_block[0]][1] != 1:
                                    break
                            except IndexError:
                                break
                        if self.selected_block[0] == -1:
                            self.selected_block = t
                elif event.type == MOUSEBUTTONDOWN:
                    what_press = pygame.mouse.get_pressed()
                    # 左键点击
                    if what_press == (1, 0, 0):
                        self.do_game(pos)
            # 改变时间
            if timer.get('second') == '1' and self.win == 0:
                # 改变记录
                f = open(game_record, 'r')
                info = f.readlines()
                f.close()
                numb = eval(info[3])[1]
                info[3] = "['游戏总时间',%d]\n" % (numb + 1)
                f = open(game_record, 'w')
                for x in info:
                    f.write(x)
                f.close()
                timer.began()
                self.time_record += 1
            # 画背景
            self.screen.blit(self.bg_picture, [0, 0])
            # 显示当前游戏
            text = self.font.render('当前游戏:%s-%s' % (self.going_kind, self.going_line), True, [0, 0, 255])
            self.screen.blit(text, [700, 20])
            # 时间
            self.screen.blit(self.time_picture, [1400, 200])
            text = self.font.render('%s:%s' % (self.time_record // 60, self.time_record % 60), True, [200, 80, 0])
            self.screen.blit(text, [1520, 270])
            # 返回按钮
            self.screen.blit(self.back_picture, [100, 50])
            # 重置按钮
            self.screen.blit(self.refresh_picture, [1500, 500])
            # 画游戏框界面
            for x in range(10):
                pygame.draw.line(self.screen, [0, 0, 0], [x * 90 + 500, 150], [x * 90 + 500, 825], 2)
                pygame.draw.line(self.screen, [0, 0, 0], [500, x * 75 + 150], [1310, x * 75 + 150], 2)
            for x in range(4):
                pygame.draw.line(self.screen, [0, 0, 0], [x * 270 + 500, 150], [x * 270 + 500, 825], 5)
                pygame.draw.line(self.screen, [0, 0, 0], [500, x * 225 + 150], [1310, x * 225 + 150], 5)
            # 画出游戏数字
            temp = 0
            for line in self.copy_game:
                mark = 0
                for num in line:
                    # 画出固定区域
                    if num[1] == 1:
                        self.screen.blit(self.transparent, [mark * 90 + 502, temp * 75 + 150])
                        text = self.font2.render(str(num[0]), True, [0, 0, 0])
                        self.screen.blit(text, [mark * 90 + 530, temp * 75 + 176])
                    # 画出数字
                    elif num[0] != 0:
                        if not self.judge_mistake(num[0], [mark, temp], self.copy_game):
                            # 标红
                            self.copy_game[temp][mark][1] = 2
                            c = [255, 0, 0]
                        else:
                            self.copy_game[temp][mark][1] = 0
                            c = [0, 0, 0]
                        text = self.font2.render(str(num[0]), True, c)
                        self.screen.blit(text, [mark * 90 + 530, temp * 75 + 176])
                    mark += 1
                temp += 1
            # 画出数字区
            for x in range(10):
                for y in self.color1:
                    self.color1[self.color1.index(y)] = rainbow(y, 0.1)
                pygame.draw.rect(self.screen, self.color1[x], [x * 90 + 450, 900, 90, 90])
                if x < 9:
                    text = self.font2.render(str(x + 1), True, [0, 0, 0])
                    self.screen.blit(text, [x * 90 + 480, 930])
            # 显示已用完的数字
            t = [0 for x in range(9)]
            for li in self.copy_game:
                for n in li:
                    if n[0] != 0:
                        t[n[0] - 1] += 1
            mark = 0
            for c in t:
                if c == 9:
                    pygame.draw.rect(self.screen, [0, 0, 0], [mark * 90 + 450, 900, 90, 90], 4)
                    self.used[mark] = 1
                else:
                    self.used[mark] = 0
                mark += 1
            # 退格
            text = self.font2.render('C', True, [0, 0, 0])
            self.screen.blit(text, [1290, 930])
            # 改变按钮颜色
            self.game_color(pos)
            if self.judge == 1:
                self.judge_win()
                self.judge = 0
            pygame.display.update()

    # 判断重复数字
    def judge_mistake(self, num, block, game):
        # 判断行
        t = 0
        row = []
        for i in game[block[1]]:
            row.append(i[0])
        for x in row:
            # 相等且不为0判断重复
            if num == x and num != 0:
                t += 1
            if t == 2:
                return False
        # 判断列
        t = 0
        column = []
        for r in game:
            column.append(r[block[0]][0])
        for x in column:
            # 相等且不为0判断重复
            if num == x and num != 0:
                t += 1
            if t == 2:
                return False
        # 判断区
        t = 0
        what_block = [block[1] // 3, block[0] // 3]
        lis = []
        for x in range(3):
            for y in range(3):
                lis.append(game[what_block[0] * 3 + x][what_block[1] * 3 + y][0])
        for x in lis:
            if num == x:
                t += 1
            if t == 2:
                return False
        return True

    # 判断获胜
    def judge_win(self):
        for line in self.copy_game:
            for i in line:
                # 有错误或没填
                if i[1] == 2 or i[0] == 0:
                    return False
        # 全部无错误
        self.win = 1
        return True

    # 存档
    def save_game(self, time):
        self.how_item[self.what_hard][1][self.going_line][1] = time
        # 刷新记录
        if self.win == 1:
            if time < self.how_item[self.what_hard][1][self.going_line][0] or self.how_item[self.what_hard][1][self.going_line][0] == 0:
                self.how_item[self.what_hard][1][self.going_line][0] = self.time_record
            self.how_item[self.what_hard][1][self.going_line][1] = 0
        f = open(data, 'w')
        f.write(str(self.how_item))
        f.close()
        # 刷新游戏界面和游戏存档
        temp = []
        for line in self.copy_game:
            mark = []
            for i in line:
                if i[1] != 1:
                    mark.append([0, 0])
                else:
                    mark.append(i)
            temp.append(mark)
        self.copy_game = temp
        f = open('./data/%s/%d.txt' % (self.going_kind, self.going_line), 'w')
        f.write(str(self.copy_game))
        f.close()

    # 游戏中的点击事件
    def do_game(self, pos):
        # 返回主页面并存入继续游戏存档和游戏存档
        if math.sqrt((pos[0] - 138) ** 2 + (pos[1] - 89) ** 2) < 38:
            self.condition = 0
            # 普通返回
            if self.win == 0:
                # data存档
                f = open(data, 'w')
                self.how_item[self.what_hard][1][self.going_line][1] = self.time_record
                f.write(str(self.how_item))
                # 游戏存档
                f = open('./data/%s/%d.txt' % (self.going_kind, self.going_line), 'w')
                f.write(str(self.copy_game))
                f.close()
            # 获胜返回
            else:
                self.save_game(self.time_record)
                # 刷新时间
                # self.time_record = 0
                self.win = 0
            # 继续游戏存档
            f = open(continue_game, 'w')
            f.write(str([self.going_kind, self.going_line]))
            f.close()
            # 还原选定格子
            self.selected_block = [-1, -1]
        # 重置游戏
        if math.sqrt((pos[0] - 1565) ** 2 + (pos[1] - 548) ** 2) < 44 and self.win == 0:
            # 刷新时间
            self.save_game(0)
            self.time_record = 0
        # 点击格子区
        if 500 < pos[0] < 1310 and 150 < pos[1] < 825 and self.win == 0:
            # 设置格子行列
            draw_pos0 = (pos[0] - 500) // 90
            draw_pos1 = (pos[1] - 150) // 75
            # 非固定区才能点击
            if self.copy_game[draw_pos1][draw_pos0][1] != 1:
                self.selected_block = [draw_pos0, draw_pos1]
        # 当选定格子时
        if self.selected_block != [-1, -1] and self.win == 0:
            # 点击数字区填入数字
            if 450 < pos[0] < 1260 and 900 < pos[1] < 990:
                num = (pos[0] - 450) // 90
                if self.used[num] == 0:
                    # 替换数字
                    self.copy_game[self.selected_block[1]][self.selected_block[0]][0] = num + 1
            # 点击退格删除数字(填入0)
            elif 1260 < pos[0] < 1390:
                self.copy_game[self.selected_block[1]][self.selected_block[0]][0] = 0
                self.mistake = 0
            self.judge = 1

    # 动态改变游戏中的按钮颜色
    def game_color(self, pos):
        self.color = rainbow(self.color, 1)
        # 返回主页面
        if math.sqrt((pos[0] - 138) ** 2 + (pos[1] - 89) ** 2) < 38:
            self.screen.blit(self.red_back_picture, [100, 50])
        # 重置按钮
        if math.sqrt((pos[0] - 1565) ** 2 + (pos[1] - 548) ** 2) < 44 and self.win == 0:
            self.screen.blit(self.refresh_red_picture, [1500, 500])
        # 没获胜时显示选定的格子
        if self.selected_block != [-1, -1] and self.win == 0:
            pygame.draw.rect(self.screen, self.color, [self.selected_block[0] * 90 + 500, self.selected_block[1] * 75 + 150, 90, 75], 4)
        # 获胜
        if self.win == 1:
            text = self.font.render('You Win!', True, [255, 0, 0])
            self.screen.blit(text, [850, 450])


shu_du = ShuDu()
shu_du.game_menu()
