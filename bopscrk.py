#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - init script

"""
Before Outset PaSsword CRacKing is a tool to assist in the previous process of cracking passwords.
"""

name =  'bopscrk.py'
__author__ = 'r3nt0n'
__version__ = '2.4'
__status__ = 'Development'


from modules.args import Arguments
from modules.config import Config


args = Arguments()
Config = Config(args.cfg_file)
Config.setup()


if __name__ == '__main__':
    from modules import main as bopscrk
    bopscrk.run()
