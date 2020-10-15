#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - parsing configuration module

import configparser

CFG_FILE = './bopscrk.cfg'  # relative to bopscrk.py path


def read_config(category, field):
    cfg = configparser.ConfigParser()
    try:
        cfg.read([CFG_FILE])
        value = cfg.get(category, field)
    except:
        value = False
    return value

def merge_settings(chars, strings):
    final_list = []
    if chars:
        final_list[:] = chars
    if strings:
        final_list.extend(strings.split())
    return final_list

def parse_booleans(value):
    if value.lower() ==  'true':
        return True
    return False

class Config:
    EXTRA_COMBINATIONS = parse_booleans(read_config('COMBINATIONS', 'extra_combinations'))
    SEPARATORS_CHARSET = merge_settings(read_config('COMBINATIONS', 'separators_chars'),
                                        read_config('COMBINATIONS', 'separators_strings'))
    LEET_CHARSET = (read_config('TRANSFORMS', 'leet_charset')).split()
    RECURSIVE_LEET = parse_booleans(read_config('TRANSFORMS', 'recursive_leet'))
    REMOVE_PARENTHESIS = parse_booleans(read_config('LYRICS', 'remove_parenthesis'))
    TAKE_INITIALS = parse_booleans(read_config('LYRICS', 'take_initials'))
    ARTIST_SPLIT_BY_WORD = parse_booleans(read_config('LYRICS', 'artist_split_by_word'))
    LYRIC_SPLIT_BY_WORD = parse_booleans(read_config('LYRICS', 'lyric_split_by_word'))
    ARTIST_SPACE_REPLACEMENT = parse_booleans(read_config('LYRICS', 'artist_space_replacement'))
    LYRIC_SPACE_REPLACEMENT = parse_booleans(read_config('LYRICS', 'lyric_space_replacement'))
    SPACE_REPLACEMENT_CHARSET = merge_settings(read_config('LYRICS', 'space_replacement_chars'),
                                               read_config('LYRICS', 'space_replacement_strings'))



