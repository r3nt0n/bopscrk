#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - combinators functions module

import itertools
from collections import OrderedDict

from lib.config import *
from lib.color import *

def add_common_separators(wordlist):
    """
    Take a wordlist and generate all possible combinations between the words
    contained and another wordlist which contains common separator (e.g. _ ).

    :param wordlist: the base wordlist to combine
    :return: a new wordlist with all the combinations
    """
    #separators = ['.', '_', '-', '123', '$', '%', '&', '#', '@']
    separators = []
    # Reading separators charset from config file
    separators_chars = read_config('COMBINATIONS', 'separators_chars')
    separators_strings = read_config('COMBINATIONS', 'separators_strings')
    if (not separators_chars) and (not separators_strings):
        print('  {}[!]{} Any separators charset specified in {}'.format(color.ORANGE, color.END,CFG_FILE))
        #sys.exit(3)
    if separators_chars:
        separators[:] = separators_chars
    if separators_strings:
        separators.extend(separators_strings.split())

    words = wordlist[:]
    new_wordlist = []
    for word in words:
        for sep in separators:
            new_wordlist.append(word + sep)
            new_wordlist.append(sep + word)

    base_wordlist_with_seps = new_wordlist[:]

    for word in words:
        for wordsep in base_wordlist_with_seps:
            if word not in wordsep:
                new_wordlist.append(wordsep + word)
                new_wordlist.append(word + wordsep)

    return list(OrderedDict.fromkeys(new_wordlist))


################################################################################
def combinator(wordlist, nWords):
    new_wordlist = wordlist[:]  # I need copy to use itertools properly
    wlist_combined = itertools.permutations(new_wordlist, nWords)
    for combination in wlist_combined:
        word = ''
        for i in combination:
            word += i
        if word not in new_wordlist: new_wordlist.append(word)
    return new_wordlist

