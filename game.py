# -*- coding: utf-8 -*-
"""
@author: Junxiao Song
"""

from __future__ import print_function
import numpy as np
import pygame

from GameMap import Map

REC_SIZE = 50  #棋盘中每个方格的边长
CHESS_RADIUS = REC_SIZE // 2 - 2  #棋子半径
CHESS_LEN = 9  #棋盘规模
MAP_WIDTH = CHESS_LEN * REC_SIZE  #棋盘宽度
MAP_HEIGHT = CHESS_LEN * REC_SIZE  #棋盘高度

INFO_WIDTH = 200  #右边显示信息宽度
BUTTON_WIDTH = 140  #按钮宽度
BUTTON_HEIGHT = 50  #按钮高度

SCREEN_WIDTH = MAP_WIDTH + INFO_WIDTH  #整个游戏界面的宽度
SCREEN_HEIGHT = MAP_HEIGHT

class Board(object):
    """board for the game"""

    def __init__(self, **kwargs):
        self.width = int(kwargs.get('width', 8))
        self.height = int(kwargs.get('height', 8))

        self.MAP_WIDTH = self.width * REC_SIZE
        self.MAP_HEIGHT = self.height * REC_SIZE
        self.SCREEN_WIDTH = self.MAP_WIDTH + INFO_WIDTH
        self.SCREEN_HEIGHT = self.MAP_HEIGHT
        # board states stored as a dict,
        # key: move as location on the board,
        # value: player as pieces type
        self.states = {}
        # need how many pieces in a row to win
        self.n_in_row = int(kwargs.get('n_in_row', 5))
        self.players = [1, 2]  # player1 and player2

    def init_board(self, start_player=0):
        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception('board width and height can not be '
                            'less than {}'.format(self.n_in_row))
        self.current_player = self.players[start_player]  # start player
        # keep available moves in a list
        self.availables = list(range(self.width * self.height))  # 棋盘上剩余落点
        self.states = {}  # 棋盘状态
        self.last_move = -1

    def move_to_location(self, move):
        """
        3*3 board's moves like:
        6 7 8
        3 4 5
        0 1 2
        and move 5's location is (1,2)
        """
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if move not in range(self.width * self.height):
            return -1
        return move

    def current_state(self):
        """return the board state from the perspective of the current player.
        state shape: 4*width*height
        """

        square_state = np.zeros((4, self.width, self.height))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == self.current_player]
            move_oppo = moves[players != self.current_player]
            square_state[0][move_curr // self.width,
                            move_curr % self.height] = 1.0
            square_state[1][move_oppo // self.width,
                            move_oppo % self.height] = 1.0
            # indicate the last move location
            square_state[2][self.last_move // self.width,
                            self.last_move % self.height] = 1.0
        if len(self.states) % 2 == 0:
            square_state[3][:, :] = 1.0  # indicate the colour to play
        return square_state[:, ::-1, :]

    def do_move(self, move):
        self.states[move] = self.current_player
        self.availables.remove(move)
        self.current_player = (
            self.players[0] if self.current_player == self.players[1]
            else self.players[1]
        )
        self.last_move = move

    def has_a_winner(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row

        moved = list(set(range(width * height)) - set(self.availables))
        if len(moved) < self.n_in_row * 2 - 1:
            return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1

    def game_end(self):
        """Check whether the game is ended or not"""
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self.availables):
            return True, -1
        return False, -1

    def get_current_player(self):
        return self.current_player

class Button():
    def __init__(self, screen, text, x, y, color, enable):
        self.screen = screen
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        self.button_color = color
        self.text_color = (255, 255, 255)
        self.enable = enable
        self.font = pygame.font.SysFont(None, BUTTON_HEIGHT * 2 // 3)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (x, y)
        self.text = text
        self.init_msg()

    #初始化信息
    def init_msg(self):
        if self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
        else:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        if self.enable:
            self.screen.fill(self.button_color[0], self.rect)
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
        else:
            self.screen.fill(self.button_color[1], self.rect)
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
        self.screen.blit(self.msg_image, self.msg_image_rect)


class StartButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, [(26, 173, 25), (158, 217, 157)], True)

    def click(self, game, player1, player2):
        if self.enable:
            game.reset()
            # game.start_play(player1, player2)
            print("clicked")
            # game.winner = None
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def unclick(self):
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True


class GiveupButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, [(230, 67, 64), (236, 139, 137)], False)

    def click(self, game, player1, player2):
        if self.enable:
            game.winner = (
            game.board.players[0] if game.board.current_player == game.board.players[1]
            else game.board.players[1]
        )
            game.is_play = False
            # game.is_play = False
            # if game.winner is None:
            #     game.winner = game.map.reverseTurn(game.player)
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def unclick(self):
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True

class Game(object):
    """game server"""

    def __init__(self, board, player1, player2, start_player=0, is_shown=1, **kwargs):
        self.board = board
        pygame.init()
        self.map = Map(self.board.width, self.board.height)
        self.screen = pygame.display.set_mode([board.SCREEN_WIDTH, board.SCREEN_HEIGHT])
        self.buttons = []
        self.buttons.append(StartButton(self.screen, 'Start', board.MAP_WIDTH + 30, 15))
        self.buttons.append(GiveupButton(self.screen, 'Giveup', board.MAP_WIDTH + 30, BUTTON_HEIGHT + 45))
        self.is_end = False
        self.is_play = False
        self.winner = -1
        self.player1 = player1
        self.player2 = player2
        self.start_player = start_player
        self.is_shown = is_shown
        p1, p2 = self.board.players
        self.player1.set_player_ind(p1)
        self.player2.set_player_ind(p2)
        self.players = {p1: player1, p2: player2}

        self.board.init_board(self.start_player)  # if start_player == 0 then current player == 1  otherwise
        self.mousePoint = None


    def graphic(self, board, player1, player2):
        """Draw the board and show game info"""
        width = board.width
        height = board.height

        print("Player", player1, "with X".rjust(3))
        print("Player", player2, "with O".rjust(3))
        print()
        for x in range(width):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                p = board.states.get(loc, -1)
                if p == player1:
                    print('X'.center(8), end='')
                elif p == player2:
                    print('O'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n')

    def gui(self):
        light_yellow = (247, 238, 214)
        pygame.draw.rect(self.screen, light_yellow, pygame.Rect(0, 0, self.board.MAP_WIDTH, self.board.SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.board.MAP_WIDTH, 0, INFO_WIDTH,
                                                                   self.board.SCREEN_HEIGHT))

        for button in self.buttons:
            button.draw()

        if self.is_end or self.winner != -1:
            self.show_winner(self.winner)

        self.map.drawBackground(self.screen)
        self.map.drawChess(self.screen)

    def mouseClick(self, map_x, map_y):
        if self.map.isInMap(map_x, map_y) and not self.is_end:
            x, y = self.map.MapPosToIndex(map_x, map_y)
            if self.map.isEmpty(x, y):
                self.mousePoint = (x, y)



    def check_buttons(self, mouse_x, mouse_y):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_x, mouse_y):
                self.click_button(button)
                break

    def click_button(self, button):
        if button.click(self, self.player1, self.player2):
            for tmp in self.buttons:
                if tmp != button:
                    tmp.unclick()

    def show_winner(self, winner):
        def showfont(screen, text, location_x, locaiton_y, height):
            font = pygame.font.SysFont(None, height)
            font_image = font.render(text, True, (0, 0, 255), (255, 255, 255))
            font_image_rect = font_image.get_rect()
            font_image_rect.x = location_x
            font_image_rect.y = locaiton_y
            screen.blit(font_image, font_image_rect)

        if winner == 1:
            str = 'Winner is Player1'
        elif winner == 2:
            str = 'Winner is Player2'
        else:
            str = 'Tie'

        showfont(self.screen, str, self.board.MAP_WIDTH + 25, self.board.SCREEN_HEIGHT - 60, 30)
        pygame.mouse.set_visible(True)


    def reset(self):
        self.is_play = True
        self.is_end = False
        self.board.init_board(self.start_player)
        self.map.reset()


    def start_play(self):
        """start a game between two players"""
        # if self.start_player not in (0, 1):
        #     raise Exception('start_player should be either 0 (player1 first) '
        #                     'or 1 (player2 first)')
        # self.board.init_board(self.start_player)  # if start_player == 0 then current player == 1  otherwise
        # # current player == 2
        # self.map.reset()
        # p1, p2 = self.board.players
        # player1.set_player_ind(p1)
        # player2.set_player_ind(p2)
        # players = {p1: player1, p2: player2}

        # if is_shown:
            # self.graphic(self.board, player1.player, player2.player)


        self.gui()
        pygame.display.update()  # pygame update
        current_player = self.board.get_current_player()
        if self.is_play and not self.is_end:
            if current_player == 1:
                # for event in pygame.event.get():
                #     if event.type == pygame.MOUSEBUTTONDOWN:
                #         mouse_x, mouse_y = pygame.mouse.get_pos()
                #         self.check_buttons(mouse_x, mouse_y, player1, player2)
                #         if self.map.isInMap(mouse_x, mouse_y) and not self.is_end:
                #                 x, y = self.map.MapPosToIndex(mouse_x, mouse_y)
                #                 location = (x, y)
                if self.mousePoint is not None:
                    self.map.click(self.mousePoint[0], self.mousePoint[1], current_player)
                    move = self.board.location_to_move(self.mousePoint)
                    self.board.do_move(move)
                    self.mousePoint = None
                # self.graphic(self.board, player1.player, player2.player)
            else:
                # if not self.is_end:
                player_in_turn = self.players[current_player]
                move = player_in_turn.get_action(self.board)
                location = self.board.move_to_location(move)
                self.map.click(location[0], location[1], current_player)
                self.board.do_move(move)

            self.is_end, self.winner = self.board.game_end()
            if self.is_end:
                self.buttons[0].enable = True

    def start_self_play_show(self, is_shown=0, temp=1e-3):
        """start a game between two players"""
        # if self.start_player not in (0, 1):
        #     raise Exception('start_player should be either 0 (player1 first) '
        #                     'or 1 (player2 first)')
        # self.board.init_board(self.start_player)  # if start_player == 0 then current player == 1  otherwise
        # # current player == 2
        # self.map.reset()
        # p1, p2 = self.board.players
        # player1.set_player_ind(p1)
        # player2.set_player_ind(p2)
        # players = {p1: player1, p2: player2}

        # if is_shown:
        # self.graphic(self.board, player1.player, player2.player)

        self.gui()
        pygame.display.update()  # pygame update
        current_player = self.board.get_current_player()
        move, move_probs = self.player2.get_action(self.board,
                                             temp=temp,
                                             return_prob=1)
        location = self.board.move_to_location(move)
        self.map.click(location[0], location[1], current_player)
        self.board.do_move(move)
        self.is_end, self.winner = self.board.game_end()
        if self.is_end:
            self.buttons[0].enable = True

                # self.graphic(self.board, player1.player, player2.player)
        # if self.is_end:
        #     self.showWinner()
        # if is_shown:
            # self.graphic(self.board, player1.player, player2.player)
        # if self.winner != -1:
        #     self.show_winner(self.winner)

                # if end:
            #     if is_shown:
            #         if winner != -1:
            #             print("Game end. Winner is", players[winner])
            #         else:
            #             print("Game end. Tie")
            #     return winner

    def start_self_play(self, player, is_shown=0, temp=1e-3):
        """ start a self-play game using a MCTS player, reuse the search tree,
        and store the self-play data: (state, mcts_probs, z) for training
        """

        self.board.init_board()
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], []
        while True:
            # self.gui()
            # pygame.display.update()
            move, move_probs = player.get_action(self.board,
                                                 temp=temp,
                                                 return_prob=1)
            # store the data
            states.append(self.board.current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.current_player)
            # perform a move
            # location = self.board.move_to_location(move)
            # self.map.click(location[0], location[1], self.board.current_player)
            self.board.do_move(move)
            if is_shown:
                self.graphic(self.board, p1, p2)
            end, winner = self.board.game_end()
            # if end:
            #     while True:
            #         self.gui()
            #         self.show_winner(winner)
            #         pygame.display.update()  # pygame update

            if end:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                # reset MCTS root node
                player.reset_player()
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player:", winner)
                    else:
                        print("Game end. Tie")
                return winner, zip(states, mcts_probs, winners_z)
