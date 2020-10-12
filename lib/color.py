#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk

from random import choice

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[33m'
    GREY = '\033[90m'
    #ORANGEBG = '\033[48;2;255;165;0m'
    END = '\033[0m'

    RAND_KEY_COLOR = [PURPLE, CYAN, DARKCYAN, YELLOW, ORANGE]
    KEY_HIGHL = choice(RAND_KEY_COLOR)