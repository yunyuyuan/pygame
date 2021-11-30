import pygame
from GameButton import Button
from alert import Window
from threading import Thread
from requests import post
pygame.init()


def count():
    json = {
        'name': 'haha',
    }
    response = post('http://127.0.0.1:5000/match', json=json, timeout=15000)


screen = pygame.display.set_mode([800, 800], 0, 32)
button = Button(screen, '', [100, 100], mod='search', hover_pic='search_hover')
window = Window(screen, [400, 400], '', 'alert1', 'pause', texts=['确定', '取消'])
Thread(target=count).start()
while 1:
    for event in pygame.event.get():
        window.time_clock(event)
        # button.drawButton()
        window.draw_window()
        pos = pygame.mouse.get_pos()
        window.change_color(pos)
        # button.changeColor(pos)
        pygame.display.update()
