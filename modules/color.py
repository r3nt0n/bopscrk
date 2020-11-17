#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk

from random import choice

class color:
    PURPLE = u'\033[95m'
    CYAN = u'\033[96m'
    DARKCYAN = u'\033[36m'
    BLUE = u'\033[94m'
    GREEN = u'\033[92m'
    YELLOW = u'\033[93m'
    RED = u'\033[91m'
    BOLD = u'\033[1m'
    UNDERLINE = u'\033[4m'
    ORANGE = u'\033[33m'
    GREY = u'\033[90m'
    #ORANGEBG = '\033[48;2;255;165;0m'
    END = u'\033[0m'

    RAND_KEY_COLOR = [PURPLE, CYAN, DARKCYAN, YELLOW, ORANGE]
    KEY_HIGHL = choice(RAND_KEY_COLOR)
