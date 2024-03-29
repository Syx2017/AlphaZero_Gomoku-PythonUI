# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

@author: Junxiao Song
"""

from __future__ import print_function
import pickle
from game import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
from policy_value_net_numpy import PolicyValueNetNumpy
import pygame
# from policy_value_net import PolicyValueNet  # Theano and Lasagne
# from policy_value_net_pytorch import PolicyValueNet  # Pytorch
# from policy_value_net_tensorflow import PolicyValueNet # Tensorflow
from policy_value_net_keras import PolicyValueNet  # Keras


class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run():
    n = 5
    width, height = 9, 9
    model_file1 = './model/current_policy_9_9_5_iteration4600.model'
    model_file2 = './model/current_policy_9_9_5_iteration50.model'

    try:
        board = Board(width=width, height=height, n_in_row=n)

        # ############### human VS AI ###################
        # load the trained policy_value_net in either Theano/Lasagne, PyTorch or TensorFlow

        best_policy1 = PolicyValueNet(width, height, model_file=model_file1)
        best_policy2 = PolicyValueNet(width, height, model_file=model_file2)
        mcts_player1 = MCTSPlayer(best_policy1.policy_value_fn, c_puct=5, n_playout=400)
        mcts_player2 = MCTSPlayer(best_policy2.policy_value_fn, c_puct=5, n_playout=400)

        # load the provided model (trained in Theano/Lasagne) into a MCTS player written in pure numpy
        # try:
        #     policy_param = pickle.load(open(model_file, 'rb'))
        # except:
        #     policy_param = pickle.load(open(model_file, 'rb'),
        #                                encoding='bytes')  # To support python3
        # best_policy = PolicyValueNetNumpy(width, height, policy_param)
        # mcts_player = MCTSPlayer(best_policy.policy_value_fn,
        #                          c_puct=5,
        #                          n_playout=400)  # set larger n_playout for better performance

        # uncomment the following line to play with pure MCTS (it's much weaker even with a larger n_playout)
        # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

        # human player, input your move in the format: 2,3
        human = Human()

        # set start_player=0 for human first
        game = Game(board, human, mcts_player1, mcts_player2, start_player=0, is_shown=1)
        #game.start_play(human, mcts_player, start_player=0, is_shown=1)
        #game.start_self_play(mcts_player, 1)

        while True:
            if game.is_selfPlay:
            #game.start_play()
                game.start_self_play_show()
            else:
                game.start_play()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    game.mouseClick(mouse_x, mouse_y)
                    game.check_buttons(mouse_x, mouse_y)

    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
