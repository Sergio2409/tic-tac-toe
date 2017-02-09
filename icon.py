#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# icon
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


class Icon(object):

    def __init__(self):
        raise NotImplementedError("You can't create instances of "
                                  "an abstract class.")

    def __repr__(self):
        return self.icon

# The icons must be implemented as Singleton pattern.


class IconX(Icon):

    def __init__(self):
        self.icon = 'X'

    def __eq__(self, other):
        if isinstance(other, IconX):
            return self.icon == other.icon
        return False


class IconO(Icon):

    def __init__(self):
        self.icon = 'O'

    def __eq__(self, other):
        if isinstance(other, IconO):
            return self.icon == other.icon
        return False
