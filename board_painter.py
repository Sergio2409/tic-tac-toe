#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# board_painter
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
import os


class BoardPainter(object):

    def __init__(self):
        self._first_row = '   {0}  |  {1}  |  {2}  \n _____|_____|_____\n'
        self._second_row = '   {0}  |  {1}  |  {2}  \n _____|_____|_____\n'
        self._third_row = '   {0}  |  {1}  |  {2}  \n      |     |     '

    def set_board(self, board):
        self.board = board

    def update_board(self, board):
        self.set_board(board)
        self.draw_board()

    def draw_board(self, display_positions=False):
        self._draw_board(display_positions=display_positions)

    def _clear_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _draw_board(self, display_positions=False):
        if display_positions:
            # This is only for display instructions
            first_row_values = range(1, 4)
            second_row_values = range(4, 7)
            third_row_values = range(7, 10)
        else:
            first_row_values = [sq.value for sq in self.board.squares[:3]]
            second_row_values = [sq.value for sq in self.board.squares[3:6]]
            third_row_values = [sq.value for sq in self.board.squares[6:9]]

        self._clear_board()

        self.first_row = self._first_row.format(*first_row_values)
        self.second_row = self._second_row.format(*second_row_values)
        self.third_row = self._third_row.format(*third_row_values)
        print("Current Board: ")
        print(self.first_row + self.second_row + self.third_row)
