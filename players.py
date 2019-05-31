#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# players
# ---------------------------------------------------------------------
# Copyright (c) 2017 Sergio Valdes Rabelo, sergiovaldes2409@gmail.com
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created on 2017-02-08

'''doc

'''

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        absolute_import as _py3_abs_import)

from utils import ensure_int, prompt_for
from icon import IconX, IconO
from analyzer import GameAnalyzer, NoviceGameAnalyzer
from or_alanalizer import SmartAnalyzer
from marco_analizer import MarcoAnalyzer
from machine_learning_analyzer import MLGameAnalyzer


class Player(object):

    def __init__(self, *args, **kwargs):
        raise Exception("You can't create instances of an Abstract class.")

    def __new__(cls, *args, **kw):
        orig = super(Player, cls)
        instance = orig.__new__(cls)
        instance.wons = 0
        instance.started = 0
        instance.moves = []
        return instance


class Human(Player):

    def __init__(self, name='Human', icon=IconX()):
        self.name = name
        self.icon = icon
        self.level = 'human'

    @staticmethod
    def _validate_input_for_play(input_value):
        try:
            number = ensure_int(input_value)
            return True if number >= 1 and number <= 9 else False
        except:
            return False

    def get_position_to_play(self):
        message = 'Enter the position to play [1 to 9].'
        return int(prompt_for(message, Human._validate_input_for_play))


class Computer(Player):

    def __init__(self, name='Computer', icon=IconO(), level='expert', knowledge_base=None):
        self.name = name + ' ' + level
        self.icon = icon
        self.wons = 0
        self.level = level
        self.analyzer = GameAnalyzer(knowledge_base=knowledge_base)
        self.novice = NoviceGameAnalyzer(knowledge_base=knowledge_base)
        #self.novice = SmartAnalyzer()
        self.oraldo_analizer = SmartAnalyzer()
        if isinstance(icon, IconX) and level == 'expert':
            self.expert = MLGameAnalyzer(knowledge_base=knowledge_base, d_set_filename='tictac_single_for_X_icon.txt', pickle_name='dict.pickleX')
        else:
            self.expert = MLGameAnalyzer(knowledge_base=knowledge_base, d_set_filename='tictac_single.txt', pickle_name='dict.pickleO')

    def activate_ostentation(self):
        pass

    def _get_position_to_play(self, board, opposed_player):
        switch_level = {
            'novice': self.novice._choose_best_move_level1,
            'smart': self.analyzer._choose_best_move_level1,
            'expert': self.expert._choose_best_move_level1
        }
        method = switch_level.get(self.level)
        return method(board, self, opposed_player)

    def get_position_to_play(self, board, opposed_player):
        #assert isinstance(self.analyzer, GameAnalyzer)
        return self._get_position_to_play(board, opposed_player)

    def store_experience(self, game_moves, oposed_player, loser_play_1st):
        self.expert.store_experience(game_moves, self, oposed_player, loser_play_1st)
