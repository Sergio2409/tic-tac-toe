#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# game_mode
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

from players import Human, Computer
from icon import IconO, IconX


class GameMode(object):

    def restart(self):
        self.player1.moves = []
        self.player2.moves = []

    def __new__(cls, *args, **kw):
        orig = super(GameMode, cls)
        instance = orig.__new__(cls, *args, **kw)
        instance.draws = 0
        return instance


class HumanVSComputer(GameMode):

    def __init__(self, knowledge_base=None):
        self.player1 = Human()
        self.player2 = Computer(knowledge_base=knowledge_base)


class HumanVSHuman(GameMode):
    def __init__(self, player1='Human Player1', player2='Human Player2'):
        self.player1 = Human(name=player1, icon=IconX())
        self.player2 = Human(name=player2, icon=IconO())


class ComputerVSComputer(GameMode):
    def __init__(self, player1='Computer1', player2='Computer2',
                 knowledge_base=None):
        self.player1 = Computer(name=player1, knowledge_base=knowledge_base)
        self.player2 = Computer(name=player2, icon=IconX(),
                                knowledge_base=knowledge_base)
