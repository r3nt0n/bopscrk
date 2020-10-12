#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - parsing configuration module

import configparser


CFG_FILE = './bopscrk.cfg'

# READING DEFAULT PARAMETERS FROM CONFIG FILE
###############################################################################
def read_config(category, field):
    cfg = configparser.ConfigParser()
    try:
        cfg.read([CFG_FILE])
        value = cfg.get(category, field)
    except:
        value = False
    return value


# GLOBAL VARIABLES
###############################################################################
LEET_CHARSET = read_config('TRANSFORMS', 'leet_charset')
# Reading spaces replacement charset from config file
space_replacement = []
space_replacement_chars = read_config('TRANSFORMS', 'space_replacement_chars')
space_replacement_strings = read_config('TRANSFORMS', 'space_replacement_strings')
if space_replacement_chars:
    space_replacement[:] = space_replacement_chars
if space_replacement_strings:
    space_replacement.extend(space_replacement_strings.split())
SPACE_REPLACEMENT = space_replacement