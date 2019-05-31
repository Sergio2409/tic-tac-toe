#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# Copyright (c) ░s░e░r░g░i░o░v░a░l░d░e░s░2░4░0░9░
# Mail: sergiovaldes2409@gmail.com
#
# All rights reserved.
#
#
"""
Module description goes here

"""
import numpy as np
import random
from build_classificator import BuiltClassificators
from utils import get_winning_positions


class MLGameAnalyzer(object):
    def __init__(self, knowledge_base=False, display_analysis=False, d_set_filename='', pickle_name=''):
        self.knowledge_base = knowledge_base
        self.WINING_POSITIONS = get_winning_positions()
        self.CORNERS = [1, 3, 7, 9]
        self.INSIDERS = [2, 4, 8, 9]
        self.CENTER = 5
        self.classifiers = BuiltClassificators.load_classifiers(d_set_filename=d_set_filename, pickle_name=pickle_name)

    def get_custom_position(self, board):
        current_position = []
        for el in board.squares:
            val = str(el.value)
            if val == 'X':
                current_position.append(1.)
            elif val == 'O':
                current_position.append(-1.)
            else:
                current_position.append(0.)
        return current_position

    def analyze_board(self, board, player, opposed_player):
        '''An game analyzer must be capable to detect at least the following
        board states:

            - Imminent win or loose in one move.
            - Check status: for
        '''
        curr_pos = self.get_custom_position(board)
        curr_pos = np.array(curr_pos)
        play_not_chosed = True
        available_moves = board._available_idexes()
        if len(available_moves) == 1:
            return available_moves[0]
        _checked_moves = []
        _copy_probas = []
        probas = []
        best_play = None
        computed = False
        _previous_best_play = None
        while best_play not in available_moves:
            if not computed:
                best_play = self.classifiers.best_classifier.predict(curr_pos.reshape(1, -1))[0]
                best_play += 1
                probas = self.classifiers.best_classifier.predict_proba(curr_pos.reshape(1, -1))[0]
                _copy_probas = probas.tolist()
                computed = True
            else:
                _checked_moves.append(best_play)
                curr_max = max(_copy_probas)
                _copy_probas[_copy_probas.index(curr_max)] = 0
                curr_max = max(_copy_probas)
                best_play = _copy_probas.index(curr_max) + 1
                if _previous_best_play and _previous_best_play == best_play:
                    best_play = available_moves[0]
                _previous_best_play = best_play
        return int(best_play)

    def _pop(self, queue):
        val = None
        try:
            val = queue.get(block=False)
        except Exception:
            pass
        return val

    def save_line(self, line_data):
        self.classifiers.add_line_to_dataset(line_data)

    def _get_line_data(self, _board, _best_play):
        line_data = '\n'
        for square in _board.squares:
            if square.is_filled:
                if square.value.icon == 'O':
                    line_data += '-1 '
                elif square.value.icon == 'X':
                    line_data += '1 '
            else:
                line_data += '0 '
        line_data += str(_best_play-1)
        return line_data

    def store_experience(self, game_moves, player, oposed_player, loser_play_1st):
        import queue
        from board import Board
        board = Board()
        from analyzer import GameAnalyzer
        _analizer = GameAnalyzer()
        _game_moves = queue.Queue()
        _board = Board()
        [_game_moves.put(el) for el in game_moves]
        if loser_play_1st:
            f_player = player
            s_player = oposed_player
        else:
            f_player = oposed_player
            s_player = player
        oposed_player_moves = []
        player_moves = []
        moves_left = True
        count = 0
        _player_real_moves = player.moves
        _opposed_player_real_moves = oposed_player.moves
        player.moves = []
        oposed_player.moves = []
        while moves_left:
            _next_play = self._pop(_game_moves)
            if _next_play:
                if _next_play in _player_real_moves:
                    # Loser player
                    if f_player == player:
                        _board = _board._gen_board(player, player.moves, oposed_player, oposed_player.moves)
                    else:
                        _board = _board._gen_board(oposed_player, oposed_player.moves, player, player.moves)
                    _best_play = _analizer.analyze_board(_board, player, oposed_player)
                    if _best_play and _best_play != _next_play and len(player.moves) >= 0:
                        # Must save new data
                        line_data = self._get_line_data(_board, _best_play)
                        self.save_line(line_data)
                        moves_left = False
                    player.moves.append(_next_play)
                    count += 1
                else:
                    # Oposed player
                    oposed_player.moves.append(_next_play)
            else:
                moves_left = False
        self.classifiers.remove_pickle_data()
        player.moves = _player_real_moves
        oposed_player = _opposed_player_real_moves


    def _choose_best_move_level1(self, board, player, opposed_player,
                                 display_analysis=False):
        '''Returns the best position to play
        '''
        return self.analyze_board(board, player, opposed_player)
