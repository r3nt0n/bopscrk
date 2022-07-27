#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - parsing configuration module

import configparser

#CFG_FILE_example = './bopscrk.cfg'  # path relative to bopscrk.py

class Config:
    def __init__(self, cfg_file):
        self.CFG_FILE = cfg_file

    def read_config(self, category, field, expected_type):
        cfg = configparser.ConfigParser()
        cfg.read([self.CFG_FILE])
            if expected_type == bool
                try: value = cfg[category].getboolean(field)
                except: value = False
            elif expected_type == 'threads'
                try: value = int(value); return value
                except ValueError: return 4  # default number of threads if error in config provided
            else # mostly str
                try: value = cfg.get(category, field)
                except: value = False
        return value

    def merge_settings(self, chars, strings):
        final_list = []
        if chars:
            final_list[:] = chars
        if strings:
            final_list.extend(strings.split())
        return final_list

    def setup(self):
        self.THREADS = self.read_config('GENERAL', 'threads', 'threads')
        self.EXTRA_COMBINATIONS = self.read_config('COMBINATIONS', 'extra_combinations', bool)
        self.SEPARATORS_CHARSET = self.merge_settings(self.read_config('COMBINATIONS', 'separators_chars', str),
                                                      self.read_config('COMBINATIONS', 'separators_strings', str))
        self.LEET_CHARSET = (self.read_config('TRANSFORMS', 'leet_charset', str)).split()
        self.RECURSIVE_LEET = self.read_config('TRANSFORMS', 'recursive_leet', bool)
        self.REMOVE_PARENTHESIS = self.read_config('LYRICS', 'remove_parenthesis', bool)
        self.TAKE_INITIALS = self.read_config('LYRICS', 'take_initials', bool)
        self.ARTIST_SPLIT_BY_WORD = self.read_config('LYRICS', 'artist_split_by_word', bool)
        self.LYRIC_SPLIT_BY_WORD = self.read_config('LYRICS', 'lyric_split_by_word', bool)
        self.ARTIST_SPACE_REPLACEMENT = self.read_config('LYRICS', 'artist_space_replacement', bool)
        self.LYRIC_SPACE_REPLACEMENT = self.read_config('LYRICS', 'lyric_space_replacement', bool)
        self.SPACE_REPLACEMENT_CHARSET = self.merge_settings(self.read_config('LYRICS', 'space_replacement_chars', str),
                                                             self.read_config('LYRICS', 'space_replacement_strings', str))
