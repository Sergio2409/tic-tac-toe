#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# knowledge_base
# ---------------------------------------------------------------------
# Copyright (c) 2017 Sergio Valdes Rabelo, sergiovaldes2409@gmail.com
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created on 2017-02-09

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        absolute_import as _py3_abs_import)
import pickle
FILE_NAME = 'knowledge_base'


class GameResult(object):

    def __init__(self, game_moves, player_won, from_pos, score):
        '''
        @param: game_moves: All game moves.

        @param: player_won: An integer value [1 or 2] representing the
        initial or second player respectively to begin to play.

        @param: from_pos: An integer representing from which position the
        evaluated result is imminent.

        @param: An integer value [1 to 10] representing the score for this
        game result for the won player. Higher values are best than lesser.
        '''
        self.game_moves = game_moves
        self.player_won = player_won
        self.from_pos = from_pos
        self.score = score


class KnowledgeBase(object):
    '''Knowledge base for `Computer` players. Must help to those player for
    chose decisions based on earlier games leading to win.

    Must be an incremental knowledge feed of games played.
    '''

    def save(self):
        if self.evaluated_game_results:
            seriaized_results = pickle.dumps(self.evaluated_game_results)
            try:
                with open(FILE_NAME, 'w') as knowledge_base_file:
                    knowledge_base_file.write(seriaized_results)
            except:
                print('No possible to store the  knowledge base!')

    def __init__(self):
        try:
            self.load_knowledge_base()
        except:
            self.evaluated_game_results = []

    def load_knowledge_base(self):
        with open(FILE_NAME, 'r') as knowledge_base_file:
            seriaized_results = knowledge_base_file.read()
        self.evaluated_game_results = pickle.loads(seriaized_results)

    def _already_exist(self, game_moves):
        '''Returns `True` if those game moves already exist else `False`.
        '''
        filtred = list(filter(lambda x: x.game_moves == game_moves,
                               self.evaluated_game_results))
        return True if len(filtred) > 0 else False

    def add_game_result(self, game_moves, player_won, from_pos, score):
        '''Add a new game result to the knowledge base.
        '''
        if not self._already_exist(game_moves):
            game_result = GameResult(game_moves, player_won, from_pos, score)
            self.evaluated_game_results.append(game_result)
