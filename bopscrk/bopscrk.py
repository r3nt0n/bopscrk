#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - init script


name = 'bopscrk.py'
desc = 'A tool to generate smart and powerful wordlists for targeted attacks'
__version__ = '2.4.5'
__author__ = 'r3nt0n'
__status__ = 'Development'


def start():
    try:
        from .modules import main
    except ImportError:
        # catching except when running python3 bopscrk.py
        # (sketchy, need some refactor)
        from modules import main

    main.run(name, __version__)


if __name__ == '__main__':
    start()