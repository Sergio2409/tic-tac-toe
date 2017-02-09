#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# tic-tac-toe
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
from board import Board
from board_painter import BoardPainter
from game_mode import (HumanVSComputer, HumanVSHuman,
                       ComputerVSComputer)
from players import Human
from utils import prompt_for, ensure_int, get_winning_positions
from exception import NotAvailableMoves, InvalidMove
from knowledge_base import KnowledgeBase


class TicTacToeGame(object):

    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self._board_painter = BoardPainter()
        self.show_instructions()
        self.load_winning_positions()
        self.new_game()

    def choose_random_player_to_start(self):
        '''Set the first player to start aleatory.
        '''
        import random
        players = [self.game_mode.player1, self.game_mode.player2]
        self.current_player = random.choice(players)

    def get_game_mode(self):
        return self._get_game_mode()

    def ask_for_player_to_start(self):
        self.first_move = False
        print('Select the first player to play:')
        message = 'Enter `1` for player1: {0}  or `2` for player2: {1}.'.format
        message = message(self.game_mode.player1.name,
                          self.game_mode.player2.name)
        _input_validator = lambda input: input == '1' or input == '2'
        choice = prompt_for(message, _input_validator)
        if choice == '1':
            self.current_player = self.game_mode.player1
        else:
            self.current_player = self.game_mode.player2

    def check_game_status(self):
        self._check_winner_status()
        self._check_draw_status()

    def _check_player_won(self, player, test_mode=False):
        '''Returns `True` if the player has won otherwise returns `False`.
        '''
        if len(player.moves) < 3:
            return False
        player_moves = set(player.moves)
        for _position in self.WINNING_POSITIONS:
            win_position = set(_position)
            if win_position.issubset(player_moves):
                if not test_mode:
                    self.won_position = _position
                    self.winner = player
                    self.update_player_won()
                return True
        return False

    def _store_game_resutl(self, player):
        '''Store the game result on the knowledge base.
        '''
        from_pos = 0  # At this time currently i don't know it.
        score = 8  # High score
        self.knowledge_base.add_game_result(self.game_moves,
                                            self._was_first_or_secord(player),
                                            from_pos, score)

    def _check_winner_status(self):
        players = [self.game_mode.player1, self.game_mode.player2]
        for player in players:
            player_won = self._check_player_won(player)
            if player_won:
                if isinstance(self.game_mode, ComputerVSComputer):
                    # Must be Imminent Win and must be added to the knowledge
                    # base.
                    self._store_game_resutl(player)
                self.display_game_result()

    def _check_draw_status(self):
        try:
            self._board.available_squares()
        except NotAvailableMoves:
            self.game_mode.draws += 1
            self.display_game_result()

    def ask_for_continue_or_exit(self):
        option = prompt_for(
            message="Press enter to restart or `q` for exit game: ")
        if option == 'q':
            self.exit_game()
        else:
            self.new_game()

    def display_current_match(self):
        match = "Match results: Player{0}: {1} VS Player{2}: {3} Draws: {4}. "
        print(match.format(
            self.game_mode.player1.name, self.game_mode.player1.wons,
            self.game_mode.player2.name, self.game_mode.player2.wons,
            self.game_mode.draws))

    def display_game_result(self):
        self._board_painter.draw_board()
        if self.winner:
            game_result = '{0}Player: {1} WONNNNN.CONGRATULATIONS!!{2}'
            game_result = game_result.format('<'*15, self.winner.name, '>'*15)
        else:
            game_result = 'Game is Draw.'

        print(game_result)
        print('Player: {0}: moves: {1}'.format(
            self.game_mode.player1.name, self.game_mode.player1.moves))
        print('Player: {0}: moves: {1}'.format(
            self.game_mode.player2.name, self.game_mode.player2.moves))
        self.display_current_match()
        self.ask_for_continue_or_exit()

    def exit_game(self, save_knowledge=False):
        self.game_is_over = True
        if save_knowledge:
            self.knowledge_base.save()
        print('Game closed!')

    def get_next_move(self):
        '''
        '''

    def fill_board_with_next_move(self):
        '''Get the next position to move from the current player and fill the
        `board` with the related `icon`.

        Returns the position related.
        '''
        ask_for_position = True
        while ask_for_position:
            if isinstance(self.current_player, Human):
                position = self.current_player.get_position_to_play()
            else:
                # Must be a computer
                position = self.current_player.get_position_to_play(
                    self._board, self.get_current_player_opposed())
            try:
                self._board.fill_square(position, self.current_player.icon)
                ask_for_position = False
            except Exception as e:
                if e.__class__ == InvalidMove:
                    print('Invalid Move!')
                else:
                    raise e
        self.update_player_moves(position)
        return position

    def load_winning_positions(self):
        self.WINNING_POSITIONS = get_winning_positions()

    def new_game(self):
        self._board = Board()
        self._board_painter.set_board(self._board)
        self.game_mode = self.get_game_mode()
        if isinstance(self.game_mode, ComputerVSComputer):
            self.choose_random_player_to_start()
        else:
            self.ask_for_player_to_start()
        self.game_is_over = False
        self.won_position = None
        self.winner = None
        self.game_status = 'Playing'
        self.game_moves = []
        self.start_game()

    def show_instructions(self, instructions_displayed=False):
        self.instructions_displayed = True
        instructions = '''
        Welcome to Tic-Tac-Toe Game
        The Board is divided into 3X3 squares and each square can be
        occupied only by one icon nought(O) or a cross(X). The board position
        must be a digit from 1 to 9 representing each square on the
        Board. These are the only valid digits to play if the square is not
        filled. Press enter to begin:'''

        self._board_painter.draw_board(display_positions=True)
        raw_input(instructions)
        # Clear console.

    def display_player_info(self):
        _info = 'Player {0}: {1} VS Player {2}: {3}'
        players_info = _info.format(
            self.game_mode.player1.name, self.game_mode.player1.icon,
            self.game_mode.player2.name, self.game_mode.player2.icon
        )
        print(players_info)
        print('Current player: {0}'.format(self.current_player.name))

    def start_game(self):
        while not self.game_is_over:
            self._board_painter.update_board(self._board)
            self.display_player_info()
            position = self.fill_board_with_next_move()
            self.game_moves.append(position)
            self.check_game_status()
            self.update_current_player()

    # TODO: Don't you see a patterns here always asking for which is the
    # current player.
    def update_player_won(self):
        if self.game_mode.player1 == self.current_player:
            self.game_mode.player1.wons += 1
        else:
            self.game_mode.player2.wons += 1

    def _was_first_or_secord(self, player):
        '''Returns `1` if the player was the first to play else `2`.
        '''
        return 1 if player.moves[0] == self.game_moves[0] else 2

    def get_current_player_opposed(self):
        if self.game_mode.player1 == self.current_player:
            return self.game_mode.player2
        else:
            return self.game_mode.player1

    def update_player_moves(self, move):
        if self.game_mode.player1 == self.current_player:
            self.game_mode.player1.moves.append(move)
        else:
            self.game_mode.player2.moves.append(move)

    def update_current_player(self):
        if self.current_player == self.game_mode.player1:
            self.current_player = self.game_mode.player2
        else:
            self.current_player = self.game_mode.player1

    @staticmethod
    def _validate_game_mode(mode):
        try:
            game_mode = ensure_int(mode)
            return True if game_mode in [1, 2, 3] else False
        except:
            return False

    def _get_game_mode(self):
        GAME_MODES = {
            1: HumanVSComputer,
            2: HumanVSHuman,
            3: ComputerVSComputer
        }
        if hasattr(self, 'game_mode'):
            self.game_mode.restart()
            return self.game_mode
        else:
            print(''' Available Game Modes:
            1. HumanVSComputer
            2. HumanVSHuman
            3. ComputerVSComputer''')
            game_mode = prompt_for(message='Chose one of the Game Mode:',
                                   input_validator=self._validate_game_mode)
            _class = GAME_MODES.get(int(game_mode))
            _param = dict(knowledge_base=self.knowledge_base)
            return _class(_param) if game_mode in [1, 3] else _class()

if __name__ == '__main__':
    TicTacToeGame()
