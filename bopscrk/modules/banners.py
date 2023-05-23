#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - banner and help functions module

from time import sleep
from random import randint

from .color import color
from .transforms import *


# Set the time interval (in secs) between printing each line
interval = 0.03

def banner(name, version, author="r3nt0n"):
    try:
        name_rand_leet = leet_transforms(name)
        name_rand_leet = name_rand_leet[randint(0, (len(name_rand_leet) - 1))]
    except:
        name_rand_leet = name
    name_rand_case = case_transforms(name)
    name_rand_case = name_rand_case[randint((len(name_rand_case) - 3), (len(name_rand_case) - 1))]
    version = version[:3]
    print('  ,----------------------------------------------------,   ,------------,')
    sleep(interval)
    print(
        f'  | [][][][][]  [][][][][]  [][][][]  [][__]  [][][][] |   |    v{color.BLUE}{version}{color.END}    |'
    )
    sleep(interval)
    print('  |                                                    |   |------------|')
    sleep(interval)
    print(
        f'  |  [][][][][][][][][][][][][][_]    [][][]  [][][][] |===| {color.RED}{name_rand_leet}{color.END} |'
    )
    sleep(interval)
    print(
        f'  |  [_][][][]{color.KEY_HIGHL}[]{color.END}[][][][]{color.KEY_HIGHL}[][]{color.END}[][][ |   [][][]  [][][][] |===| {color.BOLD}{color.RED}{name}{color.END} |'
    )
    sleep(interval)
    print(
        f'  | [][_][]{color.KEY_HIGHL}[]{color.END}[][][][][]{color.KEY_HIGHL}[]{color.END}[][][][]||     []    [][][][] |===| {color.RED}{name_rand_case}{color.END} |'
    )
    sleep(interval)
    print(
        f'  | [__][][][]{color.KEY_HIGHL}[]{color.END}[]{color.KEY_HIGHL}[]{color.END}[][][][][][__]    [][][]  [][][]|| |   |------------|'
    )
    sleep(interval)
    print(
        f'  |   [__][________________][__]              [__][]|| |   |{color.GREEN}   {author}   {color.END}|'
    )
    sleep(interval)
    print('  `----------------------------------------------------´   `------------´\n')
    sleep(interval)

def help_banner():
    print(u'  +---------------------------------------------------------------------+')
    sleep(interval)
    print(u'  | Fields can be left empty.  You can use accentuation in your words.  |')
    sleep(interval)
    print(u'  | If you enable case transforms,  won\'t matter the lower/uppercases   |')
    sleep(interval)
    print(u'  | in your input. In "others" field (interactive mode), you can write  |')
    sleep(interval)
    print(u'  | several words comma-separated (e.g.: 2C,Flipper).                   |')
    sleep(interval)
    print(u'  |                                                                     |')
    sleep(interval)
    print(u'  |                              For advanced usage and documentation:  |')
    sleep(interval)
    print(
        f'  |                                  {color.ORANGE}https://github.com/r3nt0n/bopscrk{color.END}  |'
    )
    sleep(interval)
    print(u'  +---------------------------------------------------------------------+\n')
    sleep(interval)

def bopscrk_banner():
    sleep(interval * 4)
    print('\n')
    print(
        f'{color.ORANGE}         ▄▄▄▄    ▒█████   ██▓███    ██████  ▄████▄   ██▀███   ██ ▄█▀'
    )
    sleep(interval)
    print(u'        ▓█████▄ ▒██▒  ██▒▓██░  ██▒▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒ ██▄█▒ ')
    sleep(interval)
    print(u'        ▒██▒ ▄██▒██░  ██▒▓██░ ██▓▒░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▓███▄░ ')
    sleep(interval)
    print(u'        ▒██░█▀  ▒██   ██░▒██▄█▓▒ ▒  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ▓██ █▄ ')
    sleep(interval)
    print(u'        ░▓█  ▀█▓░ ████▓▒░▒██▒ ░  ░▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒▒██▒ █▄')
    sleep(interval)
    print(u'        ░▒▓███▀▒░ ▒░▒░▒░ ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒')
    sleep(interval)
    print(u'        ▒░▒   ░   ░ ▒ ▒░ ░▒ ░     ░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░░ ░▒ ▒░')
    sleep(interval)
    print(u'         ░    ░ ░ ░ ░ ▒  ░░       ░  ░  ░  ░          ░░   ░ ░ ░░ ░')
    sleep(interval)
    print(u'         ░          ░ ░                 ░  ░ ░         ░     ░  ░')
    sleep(interval)
    print(
        f'              ░                            ░                        {color.END}'
    )
    sleep(interval)
    #sleep(interval*2)