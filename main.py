# -*- coding:utf-8 -*-

import pygame
import time
from pygame.locals import *
import MainHandler

window_height = 660
window_width = 660


def main():
    screen = pygame.display.set_mode((window_width, window_height), 0, 32)
    background = pygame.image.load("./image/background.png")
    handler = MainHandler.MainHandler(screen)
    while True:
        screen.blit(background, (0, 0))
        key_control(handler)
        handler.run()
        pygame.display.update()
        time.sleep(0.001)


def key_control(handler):
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                handler.move(MainHandler.LEFT)
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                handler.move(MainHandler.RIGHT)
            elif event.key == K_SPACE:
                print('space')
                handler.increase_direction()


if __name__ == "__main__":
    main()
