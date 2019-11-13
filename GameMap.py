from enum import IntEnum

import pygame

# GAME_VERSION = 'V1.0'
#
REC_SIZE = 50  #棋盘中每个方格的边长
CHESS_RADIUS = REC_SIZE // 2 - 2  #棋子半径
# CHESS_LEN = 9  #棋盘规模
# MAP_WIDTH = CHESS_LEN * REC_SIZE  #棋盘宽度
# MAP_HEIGHT = CHESS_LEN * REC_SIZE  #棋盘高度
#
# INFO_WIDTH = 200  #右边显示信息宽度
# BUTTON_WIDTH = 140  #按钮宽度
# BUTTON_HEIGHT = 50  #按钮高度
#
# SCREEN_WIDTH = MAP_WIDTH + INFO_WIDTH  #整个游戏界面的宽度
# SCREEN_HEIGHT = MAP_HEIGHT

#
# class MAP_ENTRY_TYPE(IntEnum):
#     MAP_EMPTY = 0,
#     MAP_PLAYER_ONE = 1,
#     MAP_PLAYER_TWO = 2,
#     MAP_NONE = 3,  # out of map range
#

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]  #初始化棋盘数组
        self.steps = []  #记录棋子落点
        self.MapWidth = self.width * REC_SIZE
        self.MapHeight = self.height * REC_SIZE

    #重置棋盘
    def reset(self):
        for y in range(self.height):
            for x in range(self.width):
                self.map[y][x] = 0
        self.steps = []

    #改变player下棋顺序
    # def reverseTurn(self, turn):
    #     if turn == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
    #         return MAP_ENTRY_TYPE.MAP_PLAYER_TWO
    #     else:
    #         return MAP_ENTRY_TYPE.MAP_PLAYER_ONE

    #寻找落点位置
    def getMapUnitRect(self, x, y):
        map_x = x * REC_SIZE
        map_y = y * REC_SIZE

        return (map_x, map_y, REC_SIZE, REC_SIZE)

    #落点位置转坐标
    def MapPosToIndex(self, map_x, map_y):
        x = map_x // REC_SIZE
        y = map_y // REC_SIZE
        return (x, y)

    #判断落点是否在棋盘内
    def isInMap(self, map_x, map_y):
        if (map_x <= 0 or map_x >= self.MapWidth or
                map_y <= 0 or map_y >= self.MapHeight):
            return False
        return True

    #判断该点是否为空
    def isEmpty(self, x, y):
        return (self.map[y][x] == 0)

    #落子并记录落点位置
    def click(self, x, y, type):
        # self.map[y][x] = type.value
        self.map[y][x] = type
        self.steps.append((x, y))

    #画棋子
    def drawChess(self, screen):
        player_one = (255, 251, 240)  # player1 on white color
        player_two = (88, 87, 86)  # player2 on gray color
        player_color = [player_one, player_two]   #棋子颜色

        font = pygame.font.SysFont(None, REC_SIZE * 2 // 3)  #定义字体
        for i in range(len(self.steps)):
            x, y = self.steps[i]
            map_x, map_y, width, height = self.getMapUnitRect(x, y)
            pos, radius = (map_x + width // 2, map_y + height // 2), CHESS_RADIUS
            turn = self.map[y][x]
            if turn == 1:
                op_turn = 2
            else:
                op_turn = 1
            pygame.draw.circle(screen, player_color[turn - 1], pos, radius)  #落子

            msg_image = font.render(str(i), True, player_color[op_turn - 1], player_color[turn - 1])  #显示序号
            msg_image_rect = msg_image.get_rect()
            msg_image_rect.center = pos
            screen.blit(msg_image, msg_image_rect)

        #最近的一步用紫色方格突出
        if len(self.steps) > 0:
            last_pos = self.steps[-1]
            map_x, map_y, width, height = self.getMapUnitRect(last_pos[0], last_pos[1])
            purple_color = (255, 0, 255)
            point_list = [(map_x, map_y), (map_x + width, map_y),
                          (map_x + width, map_y + height), (map_x, map_y + height)]
            pygame.draw.lines(screen, purple_color, True, point_list, 1)

    #绘制棋盘
    def drawBackground(self, screen):
        color = (0, 0, 0)
        for y in range(self.height):
            # draw a horizontal line
            start_pos, end_pos = (REC_SIZE // 2, REC_SIZE // 2 + REC_SIZE * y), (
            self.MapWidth - REC_SIZE // 2, REC_SIZE // 2 + REC_SIZE * y)
            if y == (self.height) // 2:
                width = 2
            else:
                width = 1
            pygame.draw.line(screen, color, start_pos, end_pos, width)

        for x in range(self.width):
            # draw a horizontal line
            start_pos, end_pos = (REC_SIZE // 2 + REC_SIZE * x, REC_SIZE // 2), (
            REC_SIZE // 2 + REC_SIZE * x, self.MapHeight - REC_SIZE // 2)
            if x == (self.width) // 2:
                width = 2
            else:
                width = 1
            pygame.draw.line(screen, color, start_pos, end_pos, width)

        '''
        rec_size = 8
        pos = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
        for (x, y) in pos:
            pygame.draw.rect(screen, color, (
            REC_SIZE // 2 + x * REC_SIZE - rec_size // 2, REC_SIZE // 2 + y * REC_SIZE - rec_size // 2, rec_size,
            rec_size))
        '''