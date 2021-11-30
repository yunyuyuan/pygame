import pygame, copy, random, math
from Vec2d import Vec2d
from pygame.locals import *
from sys import exit
from threading import *
from time import sleep
bg = './bgd.jpg'
my_plane = './plane01.png'
enemy_picture = './enemy.png'
my_bullet_picture = './bullet.png'
my_bullet_picture2 = './bullet2.png'
enemy_bullet_picture = './enemybullet.png'
boom_picture = './boom/boom.png'
fire_picture = './liaoji.png'
plan_not_defeat = './plane8888.png'
box = './box.png'
missile = './fire.png'
lock = './lock.png'
music = './bgm.mp3'
boom_music = './boom_music.ogg'
little_boss = './little_boss.png'
menu = './menu.png'
menu_began = './menu_began.png'
menu_rate = './menu_rate.png'
menu_exit = './menu_exit.png'
record = './record.txt'
record_pic = './record.png'
back = './back.png'
back_choose = './back_red.png'
pygame.init()


class Plan(object):
    def __init__(self, name):
        self.name = name
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN, 32)
        # 游戏组件
        # 背景起始坐标
        self.bg_pos = [-400, -100]
        self.bg_picture = pygame.image.load(bg).convert()
        # 鼠标移动x,y
        self.mouse_rel = [0, 0]
        # 本机帧列表
        self.my_plan_picture_lis = []
        for x in range(14):
            my_plan_picture = pygame.image.load('./fj/%d.png' % x).convert_alpha()
            self.my_plan_picture_lis.append(my_plan_picture)
        self.boom_picture = pygame.image.load(boom_picture).convert_alpha()
        # 爆炸特效的帧列表
        self.boom_frame_lis = []
        for r in range(4):
            for c in range(8):
                frame = self.boom_picture.subsurface([c * 82 + 2 * (4 - r), r * 82, 75, 82])
                self.boom_frame_lis.append(frame)
        # boss帧列表
        self.boss_now_frame = 0
        self.boss_pic_lis = []
        for x in range(11):
            pic = pygame.image.load('./boss/%d.png' % x).convert_alpha()
            self.boss_pic_lis.append(pic)
        # 各种图片
        self.fire_picture = pygame.image.load(fire_picture).convert_alpha()
        self.enemy_picture = pygame.image.load(enemy_picture).convert_alpha()
        self.my_bullet_picture = pygame.image.load(my_bullet_picture).convert_alpha()
        self.my_bullet_picture2 = pygame.image.load(my_bullet_picture2).convert_alpha()
        self.enemy_bullet_picture = pygame.image.load(enemy_bullet_picture).convert_alpha()
        self.small_plan = pygame.transform.scale(self.my_plan_picture_lis[0], (50, 35))
        self.not_defeat_picture = pygame.image.load(plan_not_defeat).convert_alpha()
        self.box_picture = pygame.image.load(box).convert_alpha()
        self.missile_picture = pygame.image.load(missile).convert_alpha()
        self.lock_picture = pygame.image.load(lock).convert_alpha()
        self.little_boss_picture = pygame.image.load(little_boss).convert_alpha()
        self.menu_picture = pygame.image.load(menu).convert_alpha()
        self.menu_began_picture = pygame.image.load(menu_began).convert_alpha()
        self.menu_rate_picture = pygame.image.load(menu_rate).convert_alpha()
        self.menu_exit_picture = pygame.image.load(menu_exit).convert_alpha()
        self.record_picture = pygame.image.load(record_pic).convert_alpha()
        self.back = pygame.image.load(back).convert_alpha()
        self.back_choose = pygame.image.load(back_choose).convert_alpha()
        # 初始化字体
        self.my_font = pygame.font.SysFont('kaiti', 22, True, True)
        # 时间标志
        # self.clock = pygame.time.Clock()
        self.time_record = 0
        # 存在的各种子弹数组
        self.my_bullets = []
        self.enemy_bullets = []
        self.missile_list = [[], []]
        # 本机子弹速度和数量
        self.my_bullet_speed = 20
        self.my_bullet_number = 1
        # 能量
        self.my_power = 1000
        self.sub_my_power = 0
        # 存在的敌机
        self.live_enemy = []
        # 正在爆炸的坐标
        self.booming_pos = []
        # 剩余生命
        self.my_life = 3
        # 初始化本机且不无敌
        self.now_my_frame = 0
        self.my_plan_pos = [900, 500]
        self.now_plan_picture = self.my_plan_picture_lis[0]
        self.is_not_defeat = 0
        # 初始化导弹数为0
        self.missile_number = 0
        # 是否找到敌机
        self.enemy_find = 0
        # 初始化得分
        self.my_count = 0
        # 道具
        self.box_list = []
        self.have_box = 0
        self.fire_time = 0
        # 初始化boss坐标，并且无boss
        self.have_boss = 0
        self.boss_pos = [800, -250]
        self.boss_do_shut = 0
        self.boss_life = 330
        # 初始化两个小boss
        self.little_boss_pos = []
        # boss左右移动方向
        self.boss_toward = -1
        # 难度值
        self.hard = 0
        # 获取排行榜
        f = open(record, 'r').read()
        self.record_lis = eval(f)
        self.draw_record = 0

    # 重新初始化信息
    def init_info(self):
        self.time_record = 0
        # 存在的各种子弹数组
        self.my_bullets = []
        self.enemy_bullets = []
        self.missile_list = [[], []]
        # 本机子弹速度和数量
        self.my_bullet_speed = 20
        self.my_bullet_number = 1
        # 能量
        self.my_power = 1000
        self.sub_my_power = 0
        # 存在的敌机
        self.live_enemy = []
        # 正在爆炸的坐标
        self.booming_pos = []
        # 剩余生命
        self.my_life = 3
        # 初始化本机且不无敌
        self.now_my_frame = 0
        self.my_plan_pos = [900, 500]
        self.now_plan_picture = self.my_plan_picture_lis[0]
        self.is_not_defeat = 0
        # 初始化导弹数为0
        self.missile_number = 0
        # 是否找到敌机
        self.enemy_find = 0
        # 初始化得分
        self.my_count = 0
        # 道具
        self.box_list = []
        self.have_box = 0
        self.fire_time = 0
        # 初始化boss坐标，并且无boss
        self.have_boss = 0
        self.boss_pos = [800, -250]
        self.boss_do_shut = 0
        self.boss_life = 330
        # 初始化两个小boss
        self.little_boss_pos = []
        # boss左右移动方向
        self.boss_toward = -1
        # 难度值
        self.hard = 0
        # 获取排行榜
        f = open(record, 'r').read()
        self.record_lis = eval(f)
        self.draw_record = 0

    # 移动本机
    def move_my_plan(self):
        rel = self.mouse_rel
        self.my_plan_pos[0] += rel[0]
        self.my_plan_pos[1] += rel[1]
        self.screen.blit(self.now_plan_picture, self.my_plan_pos)
        # if self.is_not_defeat == 0:
        self.now_plan_picture = self.my_plan_picture_lis[self.now_my_frame]
        if self.time_record % 15 == 0:
            if self.now_my_frame < 13:
                self.now_my_frame += 1
            else:
                self.now_my_frame = 0

    # 创造本机子弹
    def create_my_bullet(self):
        # 间隔某段时间就添加子弹
        if self.time_record % self.my_bullet_speed/self.my_bullet_number == 0:
            if self.my_bullet_number == 1:
                self.my_bullets.append([self.my_plan_pos[0]+68, self.my_plan_pos[1]-13, 1])
            elif self.my_bullet_number == 2:
                self.my_bullets.append([self.my_plan_pos[0]+55, self.my_plan_pos[1]-13, 2])
                self.my_bullets.append([self.my_plan_pos[0]+85, self.my_plan_pos[1]-13, 2])
        # 子弹轨迹
        for bullet in self.my_bullets:
            if bullet[1] <= 0:
                # 销毁超出范围的子弹
                self.my_bullets.remove(bullet)
            else:
                # 没超出范围则向上移动4像素
                bullet[1] -= 4
                if bullet[2] == 1:
                    self.screen.blit(self.my_bullet_picture, [bullet[0], bullet[1]])
                else:
                    self.screen.blit(self.my_bullet_picture2, [bullet[0], bullet[1]])
        # 创造僚机子弹
        if self.fire_time > 0:
            self.screen.blit(self.fire_picture, [self.my_plan_pos[0] - 80, self.my_plan_pos[1] + 30])
            if self.time_record % 20 == 0:
                self.my_bullets.append([self.my_plan_pos[0] + 8, self.my_plan_pos[1] + 30, 1])
                self.my_bullets.append([self.my_plan_pos[0] + 120, self.my_plan_pos[1] + 30, 1])
            self.fire_time -= 1
        # 如果场上没有导弹而且又敌机就创造一个导弹
        if self.missile_number > 0 and len(self.missile_list[0]) == 0 and self.enemy_find == 1:
            # 导弹起始点为当前本机坐标
            missile_pos = copy.deepcopy([self.my_plan_pos[0]+50, self.my_plan_pos[1]-60])
            self.missile_list[0] = missile_pos
            self.missile_number -= 1
        # 发射导弹
        if len(self.missile_list[0]) > 0:
            # 导弹打向敌机
            if len(self.live_enemy) > 0:
                enemy_pos = [self.live_enemy[0][0]-10, self.live_enemy[0][1]-20]
                vec = (Vec2d(enemy_pos) - Vec2d(self.missile_list[0])).normalized()
                self.missile_list[1] = vec
                # 改变导弹朝向
                angle = 270-vec.get_angle()
                toward = pygame.transform.rotate(self.missile_picture, angle)
                # 画出标记
                self.screen.blit(self.lock_picture, [enemy_pos[0]-10, enemy_pos[1]])
                self.screen.blit(toward, (self.missile_list[0]))
                self.missile_list[0][0] += self.missile_list[1][0] * 5
                self.missile_list[0][1] += self.missile_list[1][1] * 5
            else:
                # 删除该导弹并判断无敌机
                self.missile_list = [[], []]
                self.enemy_find = 0

    # 创造多种道具效果
    def show_box(self):
        # 第一种，创造两个发射普通子弹的僚机
        if self.have_box == 1:
            self.fire_time = 1500
            self.have_box = 0
        # 第二种，清屏
        elif self.have_box == 2:
            self.enemy_bullets = []
            self.have_box = 0
        # 第三种，发射跟踪导弹
        elif self.have_box == 3:
            self.missile_number = 30
            self.have_box = 0
        # 第四种，无敌
        elif self.have_box == 4:
            self.is_not_defeat = 1600
            self.have_box = 0

    # 创造敌机
    def create_enemy(self):
        # 间隔某段时间就创建新的敌机
        if self.time_record % (250-self.hard*40) == 0:
            x = random.randint(0, 1920)
            vec_x = random.randint(-1920, 1920)
            vec_y = random.randint(200, 500)
            vec_normal = Vec2d(vec_x, vec_y).normalized()
            self.live_enemy.append([x, 0, vec_normal, [vec_x, vec_y]])
            # 存在敌机
            self.enemy_find = 1
        # 移动敌机
        for enemy_pos in self.live_enemy:
            # 销毁超出范围的敌机并扣一分
            if enemy_pos[1] >= 1080:
                self.live_enemy.remove(enemy_pos)
                if self.my_count > 0:
                    self.my_count -= 1
            # 改变碰壁敌机的移动方向
            elif enemy_pos[0] < 10 or enemy_pos[0] > 1910:
                new_vec_x = 1000-enemy_pos[0]
                new_vec_y = random.randint(enemy_pos[3][1] + 200, enemy_pos[3][1] + 500)
                new_vec_normal = Vec2d(new_vec_x, new_vec_y).normalized()
                self.live_enemy[self.live_enemy.index(enemy_pos)][2] = new_vec_normal
                self.live_enemy[self.live_enemy.index(enemy_pos)][3] = [new_vec_x, new_vec_y]
        for enemy_pos in self.live_enemy:
            # 到达随机方向向量的y坐标附近就随机一个新的方向
            if enemy_pos[3][1]-30 < enemy_pos[1] < enemy_pos[3][1]+30:
                new_vec_x = random.randint(-1920, 1920)
                new_vec_y = random.randint(enemy_pos[3][1]+400, enemy_pos[3][1]+500)
                new_vec_normal = Vec2d(new_vec_x, new_vec_y).normalized()
                self.live_enemy[self.live_enemy.index(enemy_pos)][2] = new_vec_normal
                self.live_enemy[self.live_enemy.index(enemy_pos)][3] = [new_vec_x, new_vec_y]
            # 否则按单位向量移动敌机
            else:
                self.live_enemy[self.live_enemy.index(enemy_pos)][0] += self.live_enemy[self.live_enemy.index(enemy_pos)][2][0]
                self.live_enemy[self.live_enemy.index(enemy_pos)][1] += self.live_enemy[self.live_enemy.index(enemy_pos)][2][1]
        # 画出敌机
        for enemy_pos in self.live_enemy:
            # 按照飞机中心为标准
            self.screen.blit(self.enemy_picture, [enemy_pos[0]-self.enemy_picture.get_width()/2, enemy_pos[1]-self.enemy_picture.get_height()/2])

    # 创造敌机子弹
    def create_enemy_bullet(self):
        # 敌机随机概率发射朝向本机的子弹
        for enemy in self.live_enemy:
            if random.randint(0, 1600-300*self.hard) == 0:
                enemy_pos = [enemy[0]-20, enemy[1]+15]
                normal_vec = (Vec2d(self.my_plan_pos[0]+self.my_plan_picture_lis[0].get_width()/4+20, self.my_plan_pos[1]+self.my_plan_picture_lis[0].get_height()/4) - Vec2d(enemy_pos)).normalized()
                self.enemy_bullets.append([enemy_pos, normal_vec])
        # 画出子弹轨迹
        for bullet in self.enemy_bullets:
            if 0 < bullet[0][0] < 1920 and bullet[0][1] < 1080:
                bullet[0][0] += bullet[1][0]*2
                bullet[0][1] += bullet[1][1]*2
                self.screen.blit(self.enemy_bullet_picture, bullet[0])
            # 销毁超出范围的子弹
            else:
                self.enemy_bullets.remove(bullet)

    # 创建并移动小boss
    def create_little_boss(self):
        # 每25分出现一次
        if (self.my_count + 1) % 30 == 0 and self.have_boss == 0 and len(self.little_boss_pos) == 0:
            self.little_boss_pos = [[400, -100, 50], [1400, -100, 50]]
        if len(self.little_boss_pos) > 0:
            for boss in self.little_boss_pos:
                if boss[2] > 0:
                    if boss[1] < 300:
                        boss[1] += 1.5
                    else:
                        if self.time_record % (1300 - self.hard * 100) == 0:
                            Thread(target=self.little_shut).start()
                else:
                    self.little_boss_pos.remove(boss)
                self.screen.blit(self.little_boss_picture, [boss[0], boss[1]])

    # 小boss发射子弹
    def little_shut(self):
        if len(self.little_boss_pos) > 0:
            for boss in self.little_boss_pos:
                for x in range(-10, 11):
                    try:
                        angle = math.pi / 10
                        copy_pos = copy.deepcopy([boss[0] + 70, boss[1] + 80])
                        # 此处boss可能已死
                        normal_vec = Vec2d(math.cos(x * angle * (self.little_boss_pos.index(boss)*2-1)), math.sin(x * angle * (self.little_boss_pos.index(boss)*2-1))).normalized()
                        self.enemy_bullets.append([copy_pos, normal_vec])
                        sleep(0.05)
                    except ValueError:
                        pass

    # boss发射子弹
    def boss_shut(self):
        do_shut = random.randint(1, 3)
        # 防止正在发射子弹Boss不在了
        try:
            # 第一种方法,圆形
            if do_shut == 1:
                for x in range(21):
                    if self.have_boss == 1:
                        angle = math.pi / 10
                        copy_pos = copy.deepcopy([self.boss_pos[0] + 140, self.boss_pos[1] + 100])
                        normal_vec = Vec2d(math.cos(x*angle), math.sin(x*angle)).normalized()
                        self.enemy_bullets.append([copy_pos, normal_vec])
            # 第二种方法，螺旋
            elif do_shut == 2:
                for x in range(-10, 11):
                    if self.have_boss == 1:
                        angle = math.pi / 10
                        copy_pos = copy.deepcopy([self.boss_pos[0] + 140, self.boss_pos[1] + 100])
                        normal_vec = Vec2d(math.cos(x * angle * random.choice([-1, 1])), math.sin(x * angle * random.choice([-1, 1]))).normalized()
                        self.enemy_bullets.append([copy_pos, normal_vec])
                        sleep(0.05)
            # 第三种方法，来回
            elif do_shut == 3:
                for x in range(-10, 11):
                    if self.have_boss == 1:
                        angle = math.pi / 10
                        copy_pos = copy.deepcopy([self.boss_pos[0] + 140, self.boss_pos[1] + 100])
                        normal_vec = Vec2d(math.cos(x * angle * random.choice([-1, 1])), abs(math.sin(x * angle) * random.choice([-1, 1]))).normalized()
                        self.enemy_bullets.append([copy_pos, normal_vec])
                        sleep(0.1)
        except ValueError:
            pass

    # 创造boss
    def create_boss(self):
        if self.my_count > 300 and self.have_boss == 0:
            self.have_boss = 1
        if self.have_boss == 1:
            # 登场
            if self.boss_pos[1] < 60:
                it_font = pygame.font.SysFont('heiti', 60, True)
                text = it_font.render('Boss Coming!', True, (random.randint(100, 205), self.time_record % 255, random.randint(100, 200)))
                self.screen.blit(text, (800, 500))
                self.boss_pos[1] += 0.3
            else:
                if self.time_record % (800-self.hard*100) == 0:
                    Thread(target=self.boss_shut).start()
                # 左右移动
                if self.boss_pos[0] < 0 or self.boss_pos[0] > 1600:
                    self.boss_toward = self.boss_toward - 2 * self.boss_toward
                self.boss_pos[0] += self.boss_toward / 2
            self.screen.blit(self.boss_pic_lis[self.boss_now_frame], self.boss_pos)
            if self.time_record % 3 == 0:
                if self.boss_now_frame < 10:
                    self.boss_now_frame += 1
                else:
                    self.boss_now_frame = 0

    # 判断是否击中敌机
    def judge_damage_enemy(self):
        width = self.enemy_picture.get_width()
        height = self.enemy_picture.get_height()
        for bullet_pos in self.my_bullets:
            for enemy in self.live_enemy:
                # 敌机坐标
                enemy_pos = copy.deepcopy([enemy[0], enemy[1]])
                # 判断敌机是否在子弹周围
                if enemy_pos[0]-width/2-5 <= bullet_pos[0] <= enemy_pos[0]+width/2 and enemy_pos[1] <= bullet_pos[1] <= enemy_pos[1]+height:
                    # 删除击中敌机的子弹
                    try:
                        self.my_bullets.remove(bullet_pos)
                    except:
                        pass
                    # 在没有道具的情况下有概率爆出道具
                    if random.randint(1, 15) == 5 and self.have_box == 0 and len(self.box_list) == 0:
                        self.box_list.append([enemy_pos[0]-30, enemy_pos[1]-70])
                    # 向爆炸列表中添加坐标并初始化爆炸时间为0
                    try:
                        self.live_enemy.remove(enemy)
                    except ValueError:
                        pass
                    self.booming_pos.append([[enemy_pos[0]-width/2, enemy_pos[1]-height/2], 0])
                    # 得分+1
                    self.my_count += 1
                # 判断导弹是否击中敌机
                if len(self.missile_list[0]) > 0:
                    if enemy_pos[0] - width / 2 <= self.missile_list[0][0] <= enemy_pos[0] + width / 2 and enemy_pos[1] - 20 <= self.missile_list[0][1] <= enemy_pos[1] + 20:
                        # 删除该导弹
                        self.missile_list = [[], []]
                        # 在没有道具的情况下有概率爆出道具
                        if random.randint(1, 15) == 5 and self.have_box == 0 and len(self.box_list) == 0:
                            self.box_list.append([enemy_pos[0] - 30, enemy_pos[1] - 70])
                        # 向爆炸列表中添加坐标并初始化爆炸时间为0
                        try:
                            self.live_enemy.remove(enemy)
                        except ValueError:
                            pass
                        self.booming_pos.append([[enemy_pos[0] - width / 2, enemy_pos[1] - height / 2], 0])
                        # 得分+1
                        self.my_count += 1
            # 判断是否击中小boss
            if len(self.little_boss_pos) > 0:
                for boss in self.little_boss_pos:
                    if boss[0] < bullet_pos[0] < boss[0] + 160 and boss[1] < bullet_pos[1] < \
                            boss[1] + 100:
                        try:
                            self.my_bullets.remove(bullet_pos)
                        except:
                            pass
                        # 小boss血量-1
                        if boss[2] > 0:
                            boss[2] -= 1
                        else:
                            self.little_boss_pos.remove(boss)
                        self.my_count += 1
            # 判断是否击中boss
            if self.have_boss == 1:
                if self.boss_pos[0] < bullet_pos[0] < self.boss_pos[0] + 280 and self.boss_pos[1] < bullet_pos[1] < \
                        self.boss_pos[1] + 100:
                    try:
                        self.my_bullets.remove(bullet_pos)
                    except:
                        pass
                    # boss血量-1
                    self.boss_life -= 1
                    self.my_count += 1

    # 判断是否击中本机
    def judge_damage_me(self):
        width = self.enemy_picture.get_width()
        height = self.enemy_picture.get_height()
        for bullet in self.enemy_bullets:
            if self.my_plan_pos[0]+25 < bullet[0][0] < self.my_plan_pos[0]+self.my_plan_picture_lis[0].get_width()-35 and self.my_plan_pos[1]+25 < bullet[0][1] < self.my_plan_pos[1]+self.my_plan_picture_lis[1].get_height()-30:
                # 删除该子弹并添加爆炸
                self.enemy_bullets.remove(bullet)
                pos = copy.deepcopy([self.my_plan_pos[0] + self.my_plan_picture_lis[0].get_width()/3, self.my_plan_pos[1]+self.my_plan_picture_lis[0].get_height()/3])
                self.booming_pos.append([pos, 0])
                # 生命-1
                self.my_life -= 1
                # 设置无敌时间
                self.is_not_defeat = 400
                # self.my_plan_pos = [900, 800]
        # 判断撞击
        collide = 0
        # 敌机
        for enemy in self.live_enemy:
            enemy_pos = copy.deepcopy([enemy[0] - width / 2, enemy[1] - height / 2])
            if enemy_pos[0]-10 < self.my_plan_pos[0]+self.my_plan_picture_lis[0].get_width()/2 < enemy_pos[0]+60 and enemy_pos[1]-10 < self.my_plan_pos[1]+self.my_plan_picture_lis[0].get_height()/2 < enemy_pos[1]+60:
                # 向爆炸列表中添加坐标并初始化爆炸时间为0
                try:
                    self.live_enemy.remove(enemy)
                except ValueError:
                    pass
                self.booming_pos.append([enemy_pos, 0])
                collide = 1
        # 大boss
        if self.have_boss == 1:
            if self.boss_pos[0] + 40 < self.my_plan_pos[0] < self.boss_pos[0] + 240 and self.boss_pos[1] + 20 < self.my_plan_pos[1] < self.boss_pos[1] + 110:
                collide = 1
        # 小boss
        if len(self.little_boss_pos) > 0:
            for boss in self.little_boss_pos:
                if boss[0] - 80 < self.my_plan_pos[0] < boss[0] + 100 and boss[1] - 70 < self.my_plan_pos[1] < boss[1] + 60:
                    collide = 1
        if collide == 1:
            # 销毁自己
            pos = copy.deepcopy([self.my_plan_pos[0] + self.my_plan_picture_lis[0].get_width() / 3,
                                 self.my_plan_pos[1] + self.my_plan_picture_lis[0].get_height() / 3])
            self.booming_pos.append([pos, 0])
            # 生命-1
            self.my_life -= 1
            # 设置无敌时间
            self.is_not_defeat = 400
            # self.my_plan_pos = [900, 800]

    # 移动道具盒子
    def move_box(self):
        for box_pos in self.box_list:
            box_pos[1] += 1
            self.screen.blit(self.box_picture, box_pos)
            # 判断是否捡到
            if self.my_plan_pos[0]-50 < box_pos[0] < self.my_plan_pos[0]+70 and self.my_plan_pos[1]-60 < box_pos[1] < self.my_plan_pos[1]+20:
                self.box_list.remove(box_pos)
                # 随机一个道具效果
                self.have_box = random.randint(1, 4)

    # 使本机无敌
    def remove_not_defeat(self):
        if self.is_not_defeat > 0:
            self.now_plan_picture = self.not_defeat_picture
            self.is_not_defeat -= 1
        else:
            # 恢复普通状态
            pass

    # 画出背景
    def draw_bg(self):
        pos = self.mouse_rel
        x = self.bg_pos[0] - pos[0]/20
        y = self.bg_pos[1] - pos[1]/20
        self.bg_pos = [x, y]
        self.screen.blit(self.bg_picture, self.bg_pos)

    # 显示界面各信息
    def draw_info(self):
        # 显示剩余生命
        for number in range(self.my_life):
            self.screen.blit(self.small_plan, [number*50, 10])
        # 显示得分
        string = '得分 %d' % self.my_count
        submit = self.my_font.render(string, True, (150, 200, 0))
        self.screen.blit(submit, (1800, 20))
        if self.my_count < 15:
            string = '左CTRL调节难度'
            submit = self.my_font.render(string, True, (0, 200, 100))
            self.screen.blit(submit, (100, 80))
            string = '右CTRL返回主菜单'
            submit = self.my_font.render(string, True, (0, 200, 100))
            self.screen.blit(submit, (100, 100))
            string = '鼠标单击增强火力(消耗能量)'
            submit = self.my_font.render(string, True, (0, 200, 100))
            self.screen.blit(submit, (100, 120))
            string = 'ALT+F4紧急退出'
            submit = self.my_font.render(string, True, (0, 200, 100))
            self.screen.blit(submit, (100, 140))
        # 显示难度系数
        how_hard = self.my_font.render('难度 %d' % self.hard, True, (0, 50, 230))
        pygame.draw.line(self.screen, (255, 100, 0), (1850, 150), (1850, 150-self.hard*10), 10)
        pygame.draw.lines(self.screen, (0, 150, 150), True, [(1844, 100), (1856, 100), (1856, 110), (1844, 110), (1844, 120), (1856, 120), (1856, 130), (1844, 130), (1844, 140), (1856, 140), (1856, 150), (1844, 150)], 2)
        pygame.draw.line(self.screen, (0, 150, 150), (1856, 100), (1856, 150), 2)
        # 显示剩余能量
        self.screen.blit(how_hard, (1800, 50))
        how_hard = self.my_font.render('能量', True, (0, 230, 50))
        self.screen.blit(how_hard, (28, 215))
        pygame.draw.line(self.screen, (0, 50, 255), (50, 200), (50, 200-self.my_power/10), 14)
        pygame.draw.lines(self.screen, (255, 50, 0), True, [(43, 100), (58, 100), (58, 200), (43, 200)], 2)
        # 显示boss血条
        if self.boss_life > 0:
            pygame.draw.line(self.screen, (5, 250, 100), self.boss_pos, (self.boss_pos[0] + self.boss_life*1.1, self.boss_pos[1]), 13)
        # 显示小boss血条
        if len(self.little_boss_pos) > 0:
            for boss in self.little_boss_pos:
                pygame.draw.line(self.screen, (200, 250, 10), (boss[0], boss[1]), (boss[0] + boss[2]*2.5, boss[1]), 8)

    # 爆炸特效
    def boom(self):
        # 依次爆炸
        for pos in self.booming_pos:
            # 爆炸音效
            if pos[1] == 0:
                mus = pygame.mixer.Sound(boom_music)
                mus.set_volume(0.4)
                mus.play()
            # 爆炸延迟
            self.screen.blit(self.boom_frame_lis[pos[1] // 4], [pos[0][0]-10, pos[0][1]-10])
            # 删除爆炸完成的坐标
            if pos[1] < 124:
                pos[1] += 1
            else:
                self.booming_pos.remove(pos)

    # 开始主循环
    def began(self):
        # 音乐
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(50)
        # Game Over
        go_back = 2
        over = 0
        sudden_back = 0
        # 设置鼠标位置为屏幕正中间
        pygame.mouse.set_pos(960, 540)
        # 隐藏鼠标
        pygame.mouse.set_visible(False)
        while 1:
            # 还原鼠标移动
            self.mouse_rel = [0, 0]
            # 帧时间标志
            self.time_record += 1
            # time_pass = self.clock.tick()
            # pass_second = self.time_pass/1000.0
            # 判断退出
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    exit()
                elif event.type == KEYDOWN:
                    keys_press = pygame.key.get_pressed()
                    # alt+f4退出
                    if keys_press[K_LALT] and keys_press[K_F4]:
                        pygame.display.quit()
                        exit()
                    # 调节难度
                    elif keys_press[K_LCTRL]:
                        if self.hard != 5:
                            self.hard += 1
                        else:
                            self.hard = 0
                    # 退回主菜单
                    elif keys_press[K_RCTRL]:
                        sudden_back = 1
                # 使用能量
                elif event.type == MOUSEBUTTONDOWN and self.my_power > 0:
                    self.sub_my_power = 1
                elif event.type == MOUSEBUTTONUP:
                    self.my_bullet_speed = 20
                    self.my_bullet_number = 1
                    self.sub_my_power = 0
            # 消耗能量
            if self.sub_my_power == 1 and self.my_power > 0:
                self.my_bullet_speed = 10
                self.my_bullet_number = 2
                self.my_power -= 1.9
            else:
                self.my_bullet_speed = 20
                self.my_bullet_number = 1
            # 恢复能量
            if self.my_power < 1000:
                self.my_power += 0.4
            # 获取鼠标移动,超出边界不移动
            rel = pygame.mouse.get_rel()
            if 0 < self.my_plan_pos[0] + self.my_plan_picture_lis[0].get_width() / 2 + rel[0] < 1920:
                self.mouse_rel[0] = rel[0]
            if 0 < self.my_plan_pos[1] + self.my_plan_picture_lis[0].get_height() / 2 + rel[1] < 1080:
                self.mouse_rel[1] = rel[1]
            # 画出背景
            self.draw_bg()
            # 判断击中本机使之无敌
            self.remove_not_defeat()
            # 创建boss
            if self.boss_life > 0:
                self.create_boss()
            else:
                self.have_boss = 0
            self.create_little_boss()
            # 移动本机并创建子弹
            self.move_my_plan()
            self.create_enemy()
            # 创建敌机和子弹
            self.create_my_bullet()
            self.create_enemy_bullet()
            # 判断击中敌机
            self.judge_damage_enemy()
            # 无敌状态
            if self.is_not_defeat == 0:
                self.judge_damage_me()
            # 产生道具和移动道具
            self.move_box()
            self.show_box()
            # 爆炸特效
            self.boom()
            # 显示界面信息
            self.draw_info()
            # 判断结束游戏
            if self.my_life < 0 or sudden_back == 1:
                over += 1
                if go_back == 0:
                    self.broke_record()
                    # 还原各信息并退出
                    self.init_info()
                    # 还原鼠标，停止音乐
                    pygame.mouse.set_visible(True)
                    pygame.mixer.music.stop()
                    break
            if over == 1:
                if sudden_back == 0:
                    font = pygame.font.SysFont('kaiti', 50, True)
                    text = font.render('Game Over!', True, (255, 20, 50))
                    self.screen.blit(text, (790, 400))
                    text = font.render('最终得分 %d' % self.my_count, True, (255, 20, 50))
                    self.screen.blit(text, (780, 500))
                    text = font.render('%d秒后返回菜单' % go_back, True, (200, 100, 200))
                    self.screen.blit(text, (750, 600))
                    pygame.display.update()
                    sleep(2)
                go_back = 0
            if self.my_life >= 0:
                # 更新界面
                pygame.display.update()

    # 检查排行榜
    def broke_record(self):
        for item in self.record_lis:
            if self.my_count > item[0]:
                self.record_lis.insert(self.record_lis.index(item), [self.my_count, self.name])
                self.record_lis.pop(-1)
                break
        f = open(record, 'w')
        f.write(str(self.record_lis))

    # 游戏开始界面
    def game_menu(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    exit()
                elif event.type == KEYDOWN:
                    keys_press = pygame.key.get_pressed()
                    # alt+f4退出
                    if keys_press[K_LALT] and keys_press[K_F4]:
                        pygame.display.quit()
                        exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.do_something()
            self.screen.blit(self.bg_picture, self.bg_pos)
            if self.draw_record == 0:
                # 画出菜单
                self.screen.blit(self.menu_picture, [800, 500])
            else:
                # 画出排行榜
                self.screen.blit(self.record_picture, [700, 200])
                for item in self.record_lis:
                    text = self.my_font.render(item[1], True, (255, 255, 255))
                    self.screen.blit(text, [820, self.record_lis.index(item) * 87 + 220])
                    text = self.my_font.render(str(item[0]), True, (255, 255, 255))
                    self.screen.blit(text, [1000, self.record_lis.index(item) * 87 + 220])
                self.screen.blit(self.back, [300, 150])
            self.change_button()
            pygame.display.update()

    # 根据鼠标点击决定如何
    def do_something(self):
        pos = pygame.mouse.get_pos()
        if self.draw_record == 0:
            # 开始游戏
            if 800 < pos[0] < 1020 and 500 < pos[1] < 570:
                self.began()
            # 查看排行榜
            if 800 < pos[0] < 1020 and 590 < pos[1] < 650:
                self.draw_record = 1
            # 退出游戏
            if 800 < pos[0] < 1020 and 690 < pos[1] < 750:
                pygame.display.quit()
                exit()
        else:
            pos = pygame.mouse.get_pos()
            if ((pos[0] - 338)**2 + (pos[1] - 190)**2) < 1444:
                self.draw_record = 0

    # 改变按钮状态
    def change_button(self):
        pos = pygame.mouse.get_pos()
        if self.draw_record == 0:
            if 800 < pos[0] < 1020 and 500 < pos[1] < 570:
                self.screen.blit(self.menu_began_picture, [800, 500])
            if 800 < pos[0] < 1020 and 590 < pos[1] < 650:
                self.screen.blit(self.menu_rate_picture, [849, 602])
            if 800 < pos[0] < 1020 and 690 < pos[1] < 750:
                self.screen.blit(self.menu_exit_picture, [865, 697])
        else:
            pos = pygame.mouse.get_pos()
            if ((pos[0] - 338) ** 2 + (pos[1] - 190) ** 2) < 1444:
                self.screen.blit(self.back_choose, [300, 150])


# 实例化
plane = Plan('哈哈')
plane.game_menu()
