#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# analyzer
# ---------------------------------------------------------------------
# Copyright (c) 2017 Sergio Valdes Rabelo, sergiovaldes2409@gmail.com
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created on 2017-02-08
from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        absolute_import as _py3_abs_import)
import random
from utils import get_winning_positions


class GameAnalyzer(object):
    def __init__(self, knowledge_base=False, display_analysis=False):
        self.knowledge_base = knowledge_base
        self.WINING_POSITIONS = get_winning_positions()
        self.CORNERS = [1, 3, 7, 9]
        self.INSIDERS = [2, 4, 8, 9]
        self.CENTER = 5
	self.newFlag = True

    def match_move(self, player, move_number=0):
        '''Return True if the `move_number` is equal to the moves quantity of
        the player. By default match if it's the first move for the player.
        '''
        return True if len(player.moves) == move_number else False

    def analyze_board(self, board, player, opposed_player, random_play=True):
        '''An game analyzer must be capable to detect at least the following
        board states:

            - Imminent win or loose in one move.
            - Check status: for
        '''
        opening_rules = self.opening_rules(player, opposed_player)
        if opening_rules:
            return opening_rules

        win_or_loose_in_one = self.win_or_loose_in_one(board, player,
                                                       opposed_player)
        if win_or_loose_in_one:
            return win_or_loose_in_one

        available_moves = board._available_idexes()

        imminet_win_after = self.imminent_win_after(board, available_moves,
                                                    player, opposed_player)
        if imminet_win_after:
            return imminet_win_after

        if available_moves:
            if random_play:
                return random.choice(available_moves)
            else:
                return []

    def opening_rules(self, player, opposed_player):
        '''Apply some opening rules for wining approach or prevent imminent
        loose.
        '''
        if self.match_move(player) and self.match_move(opposed_player):
            # First move of the game.
            return random.choice(self.CORNERS + [self.CENTER] +
                                 [random.choice(self.INSIDERS)])
        elif self.match_move(player) and self.match_move(opposed_player, 1):
            # Second move of the game.
            if opposed_player.moves[0] in self.CORNERS or opposed_player.moves[0] in self.INSIDERS:
                return self.CENTER
            if opposed_player.moves[0] == self.CENTER:
                return random.choice(self.CORNERS)
        return []

    def win_or_loose_in_one(self, board, player, opposed_player):
        '''Returns the first one of the available moves for win or loose in
        that respective order (Win first after prevent loose). Otherwise
        returns [].
        '''
        win_in_one = self._win_in_one(board, player)
        lose_in_one = self._lose_in_one(board, opposed_player)
        if win_in_one:
            return win_in_one[0]
        elif lose_in_one:
            return lose_in_one[0]
        return []

    def imminent_win_after(self, board, available_moves, player,
                           opposed_player):
        '''Returns for player for win or returns for opposed for prevent
        loose.
        '''

        imminent_win_after = self._imminent_win_after(board, available_moves,
                                                      player)
        if imminent_win_after:
            return imminent_win_after[0]

        opposed_imminent_win_after = self._imminent_win_after(board,
                                                              available_moves,
                                                              opposed_player)

        if opposed_imminent_win_after:
            return opposed_imminent_win_after[0]
        return []

    def _win_in_one(self, board, player):
        '''Returns position(s) to play if the `player` wins on the current
        move otherwise return None. If more than one position is returned
        means that the `player` has an `Imminent win`.
        '''
        player_moves = set(player.moves)
        all_wining_pos = get_winning_positions()
        winning_moves = []
        for winning_pos in all_wining_pos:
            win_pos = None
            w_position = set(winning_pos)
            union = player_moves.intersection(w_position)
            diff = w_position.difference(player_moves)
            if len(union) > 1 and len(diff) == 1:
                win_pos = diff.pop()
                try:
                    is_position_filled = board._is_square_filled(win_pos)

                    if not is_position_filled:
                        winning_moves.append(win_pos)
                except:
                    pass
        return winning_moves

    def _lose_in_one(self, board, opposed_player):
        '''Returns the position to play for avoid lose in next move of the
        opposed player.

        If more than one position is returned  means that the `player` has an
        `Imminent loose`.

        If only one position is returned means that the `player` is in `check`
        for loose.
        '''
        return self._win_in_one(board, opposed_player)

    def _imminent_win_after(self, board, available_moves, player):
        '''If there is an imminent win after one of the available moves this
        move must be chosen.
        '''
        _board_clone = board.clone()
        imminent_win_after = []
        for index in available_moves:
            assert _board_clone.squares == board.squares
            _board_clone._fill_square(index, player.icon)
            player.moves.append(index)
            win_in_one = self._win_in_one(_board_clone, player)
            if len(win_in_one) > 1:
                imminent_win_after.append(index)
            player.moves.remove(index)
            _board_clone._clear_square(index)
        return imminent_win_after

    def _choose_best_move_level1(self, board, player, opposed_player,
                                 display_analysis=False):
        '''Returns the best position to play
        '''
        return self.analyze_board(board, player, opposed_player)


class NoviceGameAnalyzer(GameAnalyzer):

    def analyze_board(self, board, player, opposed_player):
        '''An game analyzer must be capable to detect at least the following
        board states:

            - Imminent win or loose in one move.
            - Check status: for
        '''
        available_moves = board._available_idexes()
        return random.choice(available_moves)



