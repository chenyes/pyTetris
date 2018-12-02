# -*- coding:utf-8 -*-

import shape
import random

LEVEL = 5
MAX_COLUMN = 9
MIN_COLUMN = 0
MAX_ROW = 9
DOWN = 0
LEFT = 1
RIGHT = 2
block_width = 63


class BlockBox(object):
    def __init__(self):
        self.has_block = False
        self.block = 0


class MainHandler(object):
    def __init__(self, screen):
        self.screen = screen
        self.currentShape = 0
        self.running = True
        self.blockList = []
        for x in range(10):
            row = []
            for i in range(10):
                block1 = BlockBox()
                row.append(block1)
            self.blockList.append(row)

    def create_shape(self):
        new_type = random.randint(0, 3)
        new_rotation = random.randint(0, 3)
        sh_type = shape.ShapeType(new_type)
        sh = shape.Shape(self.screen, sh_type)
        sh.shapeType.rotation = new_rotation
        return sh

    def at_bottom(self):
        for block in self.currentShape.blockList:
            self.currentShape.lineOffset = 0
            self.currentShape.update_block()
            if block.row >= 0:
                self.blockList[block.row][block.column].has_block = True
                self.blockList[block.row][block.column].block = block
            # GameOver
            if block.row == 0:
                self.running = False
        self.currentShape = self.create_shape()

    def judge(self):
        for row in self.blockList:
            is_full = True
            for i in range(10):
                if not row[i].has_block:
                    is_full = False
                    break
            if is_full:
                full_row = row[0].block.row
                for i in range(10):
                    row[i].has_block = False
                for i in range(full_row, -1, -1):
                    for x in range(10):
                        if self.blockList[i][x].has_block:
                            self.blockList[i][x].has_block = False
                            self.blockList[i + 1][x].has_block = True
                            self.blockList[i + 1][x].block = self.blockList[i][x].block
                            self.blockList[i + 1][x].block.y += block_width

    def display_all_block(self):
        for row in self.blockList:
            for box in row:
                if box.has_block:
                    self.screen.blit(box.block.image, (box.block.x, box.block.y))

    def move_down(self):
        can_remove = True
        for block in self.currentShape.blockList:
            if block.row == 0:
                if self.blockList[block.row + 1][block.column].has_block:
                    # self.blockList[block.row][block.column].has_block = True
                    # self.blockList[block.row][block.column].block = block
                    can_remove = False
                continue
            if block.row < 0:
                continue
            if block.row == MAX_ROW:
                can_remove = False
                break
            if self.blockList[block.row + 1][block.column].has_block:
                can_remove = False
                break

        if can_remove:
            self.currentShape.lineOffset += LEVEL
            if self.currentShape.lineOffset >= block_width:
                self.currentShape.lineOffset = 0
                self.currentShape.shapeType.row += 1
        else:
            self.currentShape.active = False

    def move_left(self):
        can_remove = True
        print(can_remove)
        for block in self.currentShape.blockList:
            if block.column == MIN_COLUMN:
                print('is min column')
                can_remove = False
                break
            if self.blockList[block.row][block.column - 1].has_block:
                can_remove = False
                break
            if self.blockList[block.row + 1][block.column - 1].has_block:
                can_remove = False
                break
        if can_remove:
            self.currentShape.shapeType.column -= 1

    def move_right(self):
        can_remove = True
        for block in self.currentShape.blockList:
            if block.column == MAX_COLUMN:
                can_remove = False
                break
            if self.blockList[block.row][block.column + 1].has_block:
                can_remove = False
                break
            if self.blockList[block.row + 1][block.column + 1].has_block:
                can_remove = False
                break
        if can_remove:
            self.currentShape.shapeType.column += 1
            self.display_all_block()

    def move(self, direction):
        if not self.currentShape.active:
            return
        if direction == DOWN:
            self.move_down()
        if direction == LEFT:
            self.move_left()
        if direction == RIGHT:
            self.move_right()

    def increase_direction(self):
        self.currentShape.shapeType.change_direction(self.blockList)

    def run(self):
        if self.running:
            if self.currentShape == 0:
                self.currentShape = self.create_shape()
            if self.currentShape.active:
                self.currentShape.display()
            else:
                self.at_bottom()
            self.move_down()

        self.judge()
        self.display_all_block()
