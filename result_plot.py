#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# Copyright (c) ░s░e░r░g░i░o░v░a░l░d░e░s░2░4░0░9░
# Mail: sergiovaldes2409@gmail.com
#
# All rights reserved.
#
#
"""
Module description goes here

"""
import matplotlib.pyplot as plt


class ResutlPlot(object):

    def __init__(self):
        data1 = {
            'MLPlayer1': 0,
            'MLPlayer2': 0,
            'Draws': 500,
            'MLP St.': 250,
            'RandomP St.': 250,
            'Total': 500,
        }
        data2 = {
            'MLPlayer': 0,
            'RulesPlayer': 0,
            'Draws': 500,
            'MLP St.': 250,
            'RulesP St.': 250,
            'Total': 500,
        }
        names1 = list(data1.keys())
        values1 = list(data1.values())

        names2 = list(data2.keys())
        values2 = list(data2.values())

        fig, axs = plt.subplots(1, 2, figsize=(9, 3), sharey=True)
        axs[0].bar(names1, values1, color=['green', 'red', 'yellow', 'blue', 'cyan', 'brown'])
        axs[0].title.set_text('MLPlayer VS RandomPlayer')
        axs[1].bar(names2, values2, color=['green', 'red', 'yellow', 'blue', 'cyan', 'brown'])
        axs[1].title.set_text('MLPlayer VS RulesPlayer')
        for i in range(len(values1)):
            axs[0].text(x=names1[i], y=values1[i] + 0.2, s=str(values1[i]), size=10)
            axs[1].text(x=names2[i], y=values2[i] + 0.2, s=str(values2[i]), size=10)
        fig.suptitle('Game Result Histogram')
        plt.show()

ResutlPlot()