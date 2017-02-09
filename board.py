#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# board
# ---------------------------------------------------------------------
# Copyright (c) 2017 Merchise Autrement [~º/~] and Contributors
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
from square import Square
from icon import Icon
from exception import InvalidMove, NotAvailableMoves


class Board(object):
    def __init__(self):
        self.squares = [Square() for num in range(9)]

    def _get_proper_index(self, index):
        '''Return the proper index if the provided `index` is between 1 to 9.
        If the passed is invalid returns -1.

        The index could be passed as string. But the index returned is always
        an integer.
        This method convert the index passed to the correct
        index for internal behavior. For example if 1 is passed the correct
        index is 0, but if index is 0 it's an invalid index and an exception
        is raised.
        '''
        try:
            _index = int(index)
        except:
            return -1
        is_valid_index = _index >= 1 and _index <= 9
        if is_valid_index:
            return _index - 1
        else:
            return -1

    def get_square(self, index):
        '''Returns the square at the `index` position if it's valid.
        '''
        message = 'Invalid index!: {0}'.format(index)
        proper_index = self._get_proper_index(index)
        if proper_index > -1:
            return self.squares[proper_index]
        else:
            raise IndexError(message)

    def _is_square_filled(self, index):
        '''Returns `True` if the square is filled at the provided index else
        returns `False`.

        If the index is invalid and IndexError exception is raised.
        '''
        square = self.get_square(index)
        return square.is_filled

    def _clear_square(self, index):
        '''Remove the icon to an square with the index provided this square is
        no longer filled.
        '''
        if self._is_square_filled(index):
            proper_index = self._get_proper_index(index)
            self.squares[proper_index].reset()

    def _fill_square(self, index, icon):
        '''Index must be an string or integer value representing number from
        [1 to 9].

        This conversions must be made: convert the index to Int and must be a
        number from 1 to 9 otherwise raise an IndexError.
        '''
        if self._is_square_filled(index):
            raise InvalidMove("Invalid Move!")
        else:
            proper_index = self._get_proper_index(index)
            if proper_index > -1:
                self.squares[proper_index].set_value(icon)
            else:
                raise IndexError('Invalid index!: {0}'.format(index))

    def _fill_squares(self, positions, player):
        '''Fill all squares passed trough the `positions` with player related
        icon.
        If some positions is invalid and Exception is raised.
        '''
        for index in positions:
            self._fill_square(index, player.icon)

    def _gen_board(self, player1, p1_moves, player2, p2_moves):
        '''Generate a board with the moves passed by player.

        @param: player1, player2: An instance of Player or the icon to set
        respectively.

        @param: p1_moves, p2_moves: Positions to set in the bard switch the
        player.

        Returns a board filled if valid otherwise an error is raised.
        '''
        _new_board = Board()
        _new_board._fill_squares(p1_moves, player1)
        _new_board._fill_squares(p2_moves, player2)
        return _new_board

    def clone(self):
        '''Return a new `Board` instance with the squares of the current
        `board`.
        '''
        _new_board = Board()
        for index, square in enumerate(self.squares):
            if isinstance(square.value, Icon):
                _new_board.squares[index].set_value(square.value)
        return _new_board

    def _available_idexes(self):
        '''Returns the proper idexes form squares that are not filled. If all
        are filled return [].
        '''
        indexes = [index + 1 for index, square in
                   enumerate(self.squares) if not square.is_filled]
        return indexes if len(indexes) > 0 else []

    def available_squares(self):
        available_squares = [
            square for square in self.squares if not square.is_filled]
        if len(available_squares) > 0:
            return available_squares
        else:
            raise NotAvailableMoves('All squares are filled!')

    def fill_square(self, index, icon):
        '''
        '''
        if self.available_squares():
            self._fill_square(index, icon)
