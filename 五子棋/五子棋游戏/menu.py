from 小工具.gametool.GameButton import Button


# 菜单界面
class Menu(object):
    def __init__(self, surface):
        # 初始化菜单的几个按钮
        # self.button1 = Button(surface, '单人游戏', [960, 300], font_info=['kaiti', 30, 0], font_pos_alter=[60, 20])
        self.button_play = Button(surface, '多人游戏', [surface.get_width()/2, surface.get_height()/2 - 200], font_info=['kaiti', 30, 0], font_pos_alter=[60, 20])
        self.button_room = Button(surface, '  房间', [surface.get_width()/2, surface.get_height()/2 - 100], font_info=['kaiti', 30, 0], font_pos_alter=[60, 20])
        self.button_record = Button(surface, '  数据', [surface.get_width()/2, surface.get_height()/2], font_info=['kaiti', 30, 0], font_pos_alter=[60, 20])
        self.button_set = Button(surface, '  设置', [surface.get_width()/2, surface.get_height()/2 + 100], font_info=['kaiti', 30, 0], font_pos_alter=[60, 20])
        self.button_exit = Button(surface, '  退出', [surface.get_width()/2, surface.get_height()/2 + 200], font_info=['kaiti', 30, 0], font_pos_alter=[60, 20])
        self.button_about = Button(surface, '', [200, 200], mod='query', hover_pic='query_hover')

    # 显示按钮
    def blit_button(self):
        self.button_play.drawButton()
        self.button_room.drawButton()
        self.button_record.drawButton()
        self.button_set.drawButton()
        self.button_exit.drawButton()
        self.button_about.drawButton()

    # 鼠标悬浮
    def hover_button(self, pos):
        self.button_play.changeColor(pos)
        self.button_room.changeColor(pos)
        self.button_record.changeColor(pos)
        self.button_set.changeColor(pos)
        self.button_exit.changeColor(pos)
        self.button_about.changeColor(pos)

    # 鼠标点击
    def click_button(self, pos):
        if self.button_play.isClicked(pos):
            return 'play'
        elif self.button_room.isClicked(pos):
            return 'room'
        elif self.button_record.isClicked(pos):
            return 'record'
        elif self.button_set.isClicked(pos):
            return 'set'
        elif self.button_exit.isClicked(pos):
            return 'exit'
        elif self.button_about.isClicked(pos):
            return 'about'
        else:
            return 'none'
