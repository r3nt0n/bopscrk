#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - parsing configuration module

import configparser

#CFG_FILE_example = './bopscrk.cfg'  # path relative to bopscrk.py

class Config:
    def __init__(self, cfg_file):
        self.CFG_FILE = cfg_file
        self.cfg = configparser.ConfigParser(strict=False)

    def read_config(self, category, field):
        try:
            self.cfg.read([self.CFG_FILE])
            value = self.cfg.get(category, field)
        except Exception as e:
            print(e)
            value = False
        return value

    def merge_settings(self, chars, strings):
        final_list = []
        if chars:
            final_list[:] = chars
        if strings:
            final_list.extend(strings.split())
        return final_list

    def parse_booleans(self, value):
        try:
            if value.lower() == 'true':
                return True
            return False
        except AttributeError:
            return None

    def setup(self):
        self.EXTRA_COMBINATIONS = self.parse_booleans(self.read_config('COMBINATIONS', 'extra_combinations'))
        self.SEPARATORS_CHARSET = self.merge_settings(self.read_config('COMBINATIONS', 'separators_chars'),
                                                      self.read_config('COMBINATIONS', 'separators_strings'))
        self.LEET_CHARSET = (self.read_config('TRANSFORMS', 'leet_charset')).split()
        self.RECURSIVE_LEET = self.parse_booleans(self.read_config('TRANSFORMS', 'recursive_leet'))
        self.EXTENSIVE_CASE = self.parse_booleans(self.read_config('TRANSFORMS', 'extensive_case'))
        self.REMOVE_PARENTHESIS = self.parse_booleans(self.read_config('LYRICS', 'remove_parenthesis'))
        self.TAKE_INITIALS = self.parse_booleans(self.read_config('LYRICS', 'take_initials'))
        self.ARTIST_SPLIT_BY_WORD = self.parse_booleans(self.read_config('LYRICS', 'artist_split_by_word'))
        self.LYRIC_SPLIT_BY_WORD = self.parse_booleans(self.read_config('LYRICS', 'lyric_split_by_word'))
        self.ARTIST_SPACE_REPLACEMENT = self.parse_booleans(self.read_config('LYRICS', 'artist_space_replacement'))
        self.LYRIC_SPACE_REPLACEMENT = self.parse_booleans(self.read_config('LYRICS', 'lyric_space_replacement'))
        self.SPACE_REPLACEMENT_CHARSET = self.merge_settings(self.read_config('LYRICS', 'space_replacement_chars'),
                                                             self.read_config('LYRICS', 'space_replacement_strings'))
