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
from analyzer import GameAnalyzer


class Player(object):

    def __init__(self):
        raise Exception("You can't create instances of an Abstract class.")

    def __new__(cls, *args, **kw):
        orig = super(Player, cls)
        instance = orig.__new__(cls, *args, **kw)
        instance.wons = 0
        instance.moves = []
        return instance


class Human(Player):

    def __init__(self, name='Human', icon=IconX()):
        self.name = name
        self.icon = icon

    @staticmethod
    def _validate_input_for_play(input_value):
        try:
            number = ensure_int(input_value)
            return True if number >= 1 or number <= 9 else False
        except:
            return False

    def get_position_to_play(self):
        message = 'Enter the position to play [1 to 9].'
        return int(prompt_for(message, Human._validate_input_for_play))


class Computer(Player):

    def __init__(self, name='Computer', icon=IconO(), ostentation=False,
                 level='novice', knowledge_base=None):
        self.name = name
        self.icon = icon
        self.wons = 0
        self.level = level
        self.analyzer = GameAnalyzer(knowledge_base=knowledge_base)

    def activate_ostentation(self):
        pass

    def _get_position_to_play(self, board, opposed_player):
        switch_level = {
            'novice': self.analyzer._choose_best_move_level1,
            'smart': self.analyzer._choose_best_move_level1,
            'impossible': self.analyzer._choose_best_move_level1
        }
        method = switch_level.get(self.level)
        return method(board, self, opposed_player)

    def get_position_to_play(self, board, opposed_player):
        assert isinstance(self.analyzer, GameAnalyzer)
        return self._get_position_to_play(board, opposed_player)
