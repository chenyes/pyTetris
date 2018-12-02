# -*- coding:utf-8 -*-

import pygame

rotation_0 = 0
rotation_90 = 1
rotation_180 = 2
rotation_270 = 3

shape_type_0 = 0
shape_type_1 = 1
shape_type_2 = 2
shape_type_3 = 3

screen_border = 15

block_width = 63


class Block(object):
    def __init__(self, screen):
        self.row = 0
        self.column = 0
        self.x = 0
        self.y = 0
        self.screen = screen
        self.image = pygame.image.load("./image/block_purple.png")

    def set_position(self, row, column):
        self.row = row
        self.column = column

    def update(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.screen.blit(self.image, (self.x, self.y))


class ShapeType(object):
    def __init__(self, type_index):
        self.row = -4
        self.column = 4
        self.columnOffset = []
        self.rowOffset = []
        self.rotation = rotation_0
        self.shapeType = type_index
        self.init()

    def init(self):
        if self.shapeType == shape_type_0:
            self.update_shape_type_0()
        if self.shapeType == shape_type_1:
            self.update_shape_type_1()
        if self.shapeType == shape_type_2:
            self.update_shape_type_2()
        if self.shapeType == shape_type_3:
            self.update_shape_type_3()

    def update_shape_type_0(self):
        if self.rotation == rotation_0:
            self.rowOffset = [0, 0, 1, 2]
            self.columnOffset = [0, 1, 0, 0]
            return
        if self.rotation == rotation_90:
            self.rowOffset = [0, 0, 0, 1]
            self.columnOffset = [0, 1, 2, 2]
            return
        if self.rotation == rotation_180:
            self.rowOffset = [0, 1, 2, 2]
            self.columnOffset = [1, 1, 0, 1]
            return
        if self.rotation == rotation_270:
            self.rowOffset = [0, 1, 1, 1]
            self.columnOffset = [0, 0, 1, 2]
            return

    def update_shape_type_1(self):
        self.rowOffset = [0, 0, 1, 1]
        self.columnOffset = [0, 1, 0, 1]

    def update_shape_type_2(self):
        if self.rotation == rotation_0:
            self.rowOffset = [0, 1, 1, 1]
            self.columnOffset = [1, 0, 1, 2]
            return
        if self.rotation == rotation_90:
            self.rowOffset = [0, 1, 1, 2]
            self.columnOffset = [0, 0, 1, 0]
            return
        if self.rotation == rotation_180:
            self.rowOffset = [0, 0, 0, 1]
            self.columnOffset = [0, 1, 2, 1]
            return
        if self.rotation == rotation_270:
            self.rowOffset = [0, 1, 1, 2]
            self.columnOffset = [1, 0, 1, 1]
            return

    def update_shape_type_3(self):
        if self.rotation == rotation_0 or self.rotation == rotation_180:
            self.rowOffset = [0, 1, 2, 3]
            self.columnOffset = [0, 0, 0, 0]
            return
        if self.rotation == rotation_90 or self.rotation == rotation_270:
            self.rowOffset = [0, 0, 0, 0]
            self.columnOffset = [0, 1, 2, 3]
            return

    def change_direction(self, blockList):
        target_rotation = self.rotation + 1 if self.rotation < 4 else 0

        new_type = ShapeType(self.shapeType)
        new_type.rotation = target_rotation
        new_type.init()

        for i in range(4):
            target_row = self.row + new_type.rowOffset[i]
            target_column = self.column + new_type.columnOffset[i]
            if target_row > 9 or target_column < 0 or target_column > 9:
                return
            if blockList[target_row][target_column].has_block:
                return
        self.rotation = target_rotation
        self.init()


class Shape(object):
    def __init__(self, screen, shape_type):
        self.screen = screen
        self.shapeType = shape_type
        self.active = True
        self.lineOffset = 0
        self.blockList = []
        self.init_block()

    def init_block(self):
        for i in range(4):
            self.blockList.append(Block(self.screen))
        self.update_block()

    def update_block(self):
        for i in range(4):
            target_row = self.shapeType.row + self.shapeType.rowOffset[i]
            target_column = self.shapeType.column + self.shapeType.columnOffset[i]
            self.blockList[i].set_position(target_row, target_column)

    def display(self):
        if self.shapeType == shape_type_0:
            self.shapeType.update_shape_type_0()
        if self.shapeType == shape_type_1:
            self.shapeType.update_shape_type_1()
        if self.shapeType == shape_type_2:
            self.shapeType.update_shape_type_2()
        if self.shapeType == shape_type_3:
            self.shapeType.update_shape_type_3()
        self.update_block()
        for block in self.blockList:
            target_x = block.column * block_width + screen_border
            target_y = block.row * block_width + screen_border + self.lineOffset
            block.update(target_x, target_y)


