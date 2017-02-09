#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# square
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
from icon import Icon


class Square(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.is_filled = False
        self.value = ' '

    def set_value(self, icon):
        if isinstance(icon, Icon):
            self.value = icon
            self.is_filled = True
        else:
            raise TypeError('Only icons are set to a board square.')

    def __eq__(self, other):
        return self.value == other.value
