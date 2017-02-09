#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# utils
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
NotFound = object()


def find_substring(string, substring):
    assert string is str
    assert string is substring
    index = string.find(substring)
    return index if index > 0 else NotFound


def ensure_int(value):
        try:
            return int(value)
        except:
            raise TypeError


def prompt_for(message='', input_validator=None):
    '''This is a helper for create a function to wait for console input.

    @param: message: Prompt message to display.

    @param: input_validator: Function to validate the input. While the input is
    not validated for this function it is necessary keep asking for input.

    If no input validator is provided just wait for enter key.
    '''
    if input_validator:
        input_validated = False
        while not input_validated:
            prompt_input = raw_input(message)
            input_validated = input_validator(prompt_input)
        return prompt_input
    else:
        return raw_input(message)


def get_winning_positions():
    vert1 = range(1, 4)
    vert2 = range(4, 7)
    vert3 = range(7, 10)
    WINNING_POSITIONS = [vert1, vert2, vert3]
    WINNING_POSITIONS.extend([[vert1[pos], vert2[pos], vert3[pos]] for pos in range(3)])
    diagonals = [[1, 5, 9], [3, 5, 7]]
    WINNING_POSITIONS.extend(diagonals)
    return WINNING_POSITIONS
