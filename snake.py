from random import randint, choice
from copy import deepcopy
from time import sleep, process_time
import pygame
from pygame.locals import *
pygame.init()


class Snake(object):
    def __init__(self):
        self.screen = pygame.display.set_mode([800, 600], 0, 32)
        self.font = pygame.font.SysFont('kaiti', 25, False)
        # 蛇身
        self.snake_body = [[10, 5], [10, 6], [10, 7]]
        # 食物
        self.food = []
        self.create_food()
        # 路径
        self.now_direct = None
        # 循环次数
        self.record = 0
        # 速度
        self.speed = 10
        # 得分
        self.count = 0

    # 绘制
    def plot(self):
        # 蛇头
        pygame.draw.rect(self.screen, [255, 200, 200], [30+self.snake_body[0][0]*20+self.snake_body[0][0]*5, 30+self.snake_body[0][1]*20+self.snake_body[0][1]*5, 20, 20])
        # 蛇身
        for i in range(1, len(self.snake_body)):
            x = self.snake_body[i - 1][0] - self.snake_body[i][0]
            y = self.snake_body[i - 1][1] - self.snake_body[i][1]
            coor_x = 30+self.snake_body[i][0]*20+self.snake_body[i][0]*5
            coor_y = 30+self.snake_body[i][1]*20+self.snake_body[i][1]*5
            width = 20 + abs(x) * 5
            height = 20 + abs(y) * 5
            if x < 0:
                coor_x = 30 + self.snake_body[i][0] * 20 + self.snake_body[i][0] * 5 - abs(x) * 5
            if y < 0:
                coor_y = 30 + self.snake_body[i][1] * 20 + self.snake_body[i][1] * 5 - abs(y) * 5
            pygame.draw.rect(self.screen, [255, 255, 255], [coor_x, coor_y, width, height])
        # 边界
        pygame.draw.rect(self.screen, [0, 0, 255], [25, 25, 525, 525], 2)
        # 速度
        self.screen.blit(self.font.render('速度:%d' % self.speed, False, [255, 255, 255]), [600, 100])
        # 得分
        self.screen.blit(self.font.render('得分:%d' % self.count, False, [255, 255, 255]), [600, 300])
        # 食物
        pygame.draw.circle(self.screen, [255, 255, 255], [40+self.food[0]*20+self.food[0]*5,
                                                          40+self.food[1]*20+self.food[1]*5], 10)

    # 判断某点能移动的方向
    def find_direct(self, pos, virtual_snake=None):
        if virtual_snake:
            snake_body = virtual_snake
        else:
            snake_body = self.snake_body
        dir_lis = [[0, -1], [0, 1], [1, 0], [-1, 0]]
        lis = []
        for coordinate in dir_lis:
            head_pos = [pos[0] + coordinate[0], pos[1] + coordinate[1]]
            # 是否超出边界,移动处是否有蛇身
            if 0 <= head_pos[0] <= 20 and 0 <= head_pos[1] <= 20 and head_pos not in snake_body:
                    lis.append(head_pos)
        return lis

    # 往某方向移动一格
    def move_one(self, x, y, virtual_snake=None):
        if virtual_snake:
            snake_body = virtual_snake
        else:
            snake_body = self.snake_body
            self.record += 1
        new_head = [x, y]
        # 移动
        snake_body.insert(0, new_head)
        # 移动处没有食物
        if not new_head == self.food:
            snake_body.pop()
        # 有食物，吃掉
        elif not virtual_snake:
            self.record = 0
            self.count += 1
            # 新食物
            self.create_food()
        if virtual_snake:
            return virtual_snake

    # 创造食物
    def create_food(self):
        maps = []
        for x in range(21):
            for y in range(21):
                if [x, y] not in self.snake_body:
                    maps.append([x, y])
        if len(maps) > 1:
            while 1:
                rand_num = choice(maps)
                if abs(self.snake_body[0][0] - rand_num[0]) + abs(self.snake_body[0][1] - rand_num[1]) == 1\
                   and abs(self.snake_body[-1][0]-rand_num[0])+abs(self.snake_body[-1][1]-rand_num[1]) == 1:
                    continue
                else:
                    self.food = [rand_num[0], rand_num[1]]
                    break
        else:
            rand_num = choice(maps)
            self.food = [rand_num[0], rand_num[1]]

    # 计算某点的f值
    @staticmethod
    def cal_f(go, stop, purpose):
        # 两点的距离
        h = abs(go[0] - stop[0]) + abs(go[1] - stop[1])
        # stop到终点的距离
        g = abs(purpose[0] - stop[0]) + abs(purpose[1] - stop[1])
        return h + g

    # 检查能否看到蛇尾
    def look_tail(self, start_pos, tail_pos, virtual_snake=None):
        # open和close
        open_list = [[start_pos, self.cal_f(start_pos, start_pos, tail_pos), None]]
        close_list = []
        end_pos = self.find_direct(tail_pos, virtual_snake)
        if virtual_snake:
            if start_pos in end_pos:
                return True
        # 循环计算并选择open_list中的最小的F
        while 1:
            # 如果open表空了，则寻路失败
            if not open_list:
                return False
            # 从OPEN表中取f最小的节点small_item
            small_item = open_list[0]
            small_i = 0
            for i in range(len(open_list)):
                if open_list[i][1] < small_item[1]:
                    small_item = open_list[i]
                    small_i = i
            open_list.pop(small_i)
            # 把small_item加入到close
            close_list.append(small_item)
            # 和终点重合了,结束
            if small_item[0] in end_pos:
                if virtual_snake:
                    return True
                close_list.append(small_item)
                # 寻路成功,规划路径
                path = []
                now_pos = tail_pos
                condi = True
                while condi:
                    for item in close_list:
                        if item[0] == now_pos:
                            path.insert(0, item[0])
                            if item[2]:
                                now_pos = item[2]
                            else:
                                condi = False
                            break
                return path[1]
            # 遍历small_item能到达的节点pos
            stops_list = self.find_direct(small_item[0], virtual_snake=virtual_snake)
            for pos in stops_list:
                # 若pos在close
                if pos in [x[0] for x in close_list]:
                    continue
                # 计算f
                now_f = self.cal_f(start_pos, pos, tail_pos)
                for i in range(len(open_list)):
                    # 若在open_list
                    if pos == open_list[i][0]:
                        # 若f小于open_list中该点的的f
                        if now_f < open_list[i][1]:
                            # 把small_item设置为pos的父亲
                            open_list[i][2] = small_item[0]
                            # 更新f
                            open_list[i][1] = now_f
                # 不在open_list
                if pos not in [x[0] for x in open_list]:
                    open_list.append([pos, now_f, small_item[0]])

    # 找一个最远离食物的方向,且能看到蛇尾
    def random_direct(self, start_pos, plan_pos=None):
        # 寻路成功，检查预定路径能否看到尾巴
        if plan_pos:
            # 虚拟移动
            temp_snake = deepcopy(self.snake_body)
            temp_snake = self.move_one(plan_pos[0], plan_pos[1], virtual_snake=temp_snake)
            if self.look_tail(temp_snake[0], temp_snake[-1], virtual_snake=temp_snake):
                return plan_pos
        # 寻路失败，找一个能看到尾巴并且离食物最远的路径
        all_direct = self.find_direct(start_pos)
        can_direct = []
        max_distance = -1
        max_direct = all_direct[0]
        for direct in all_direct:
            temp_snake = deepcopy(self.snake_body)
            temp_snake = self.move_one(direct[0], direct[1], virtual_snake=temp_snake)
            if self.look_tail(temp_snake[0], temp_snake[-1], virtual_snake=temp_snake):
                distance = abs(direct[0]-self.food[0])+abs(direct[1]-self.food[1])
                if distance >= max_distance:
                    max_distance = distance
                    max_direct = direct
                    can_direct.append(direct)
        if self.record > 400:
            for i in all_direct:
                temp_snake = deepcopy(self.snake_body)
                temp_snake = self.move_one(i[0], i[1], virtual_snake=temp_snake)
                if self.find_direct(i, temp_snake) and i != max_direct:
                    print('随机')
                    return i
        return max_direct

    # 自动寻路
    def choose_direct(self):
        # 起始点
        start_pos = self.snake_body[0]
        # open和close
        open_list = [[start_pos, self.cal_f(start_pos, start_pos, self.food), None]]
        close_list = []
        # 循环计算并选择open_list中的最小的F
        while 1:
            # 如果open表空了，则寻路失败
            if not open_list:
                self.now_direct = self.random_direct(start_pos)
                return
            # 从OPEN表中取f最小的节点small_item
            small_item = open_list[0]
            small_i = 0
            for i in range(len(open_list)):
                if open_list[i][1] < small_item[1]:
                    small_item = open_list[i]
                    small_i = i
            open_list.pop(small_i)
            # 把small_item加入到close
            close_list.append(small_item)
            # 和终点重合了,结束
            if small_item[0] == self.food:
                close_list.append(small_item)
                # 寻路成功,规划路径
                path = []
                now_pos = self.food
                condi = True
                while condi:
                    for item in close_list:
                        if item[0] == now_pos:
                            path.insert(0, item[0])
                            if item[2]:
                                now_pos = item[2]
                            else:
                                condi = False
                            break
                self.now_direct = self.random_direct(start_pos, path[1])
                return
            # 遍历small_item能到达的节点pos
            stops_list = self.find_direct(small_item[0])
            for pos in stops_list:
                # 若pos在close
                if pos in [x[0] for x in close_list]:
                    continue
                # 计算f
                now_f = self.cal_f(start_pos, pos, self.food)
                for i in range(len(open_list)):
                    # 若在open_list
                    if pos == open_list[i][0]:
                        # 若f小于open_list中该点的的f
                        if now_f < open_list[i][1]:
                            # 把small_item设置为pos的父亲
                            open_list[i][2] = small_item[0]
                            # 更新f
                            open_list[i][1] = now_f
                # 不在open_list
                if pos not in [x[0] for x in open_list]:
                    open_list.append([pos, now_f, small_item[0]])

    # 开始游戏
    def start(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                if event.type == KEYDOWN:
                    key_press = pygame.key.get_pressed()
                    if key_press[K_LCTRL]:
                        if self.speed == 0:
                            self.speed = 10
                        else:
                            self.speed -= 2
            start = process_time()
            self.screen.fill([0, 0, 0])
            # sleep(0.04)
            self.choose_direct()
            # 取出一个规划的坐标
            self.move_one(self.now_direct[0], self.now_direct[1])
            self.plot()
            stop = round(process_time()-start, 3)
            if self.speed != 0:
                if self.speed/100-stop > 0:
                    sleep(self.speed/100-stop)
            pygame.display.update()


snake = Snake()
snake.start()
