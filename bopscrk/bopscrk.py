#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - init script

#import sys, os, datetime

"""
Before Outset PaSsword CRacKing is a tool to assist in the previous process of cracking passwords.
"""

name = 'bopscrk.py'
__author__ = 'r3nt0n'
__version__ = '2.4.3'
__status__ = 'Development'


def start():
    try:
        from .modules import main
    # catching except when running python3 bopscrk.py (sketchy, need some refactor)
    except ImportError:
        from modules import main
    main.run(name, __version__)


if __name__ == '__main__':
    start()