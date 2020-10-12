#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - combinators functions module

import itertools
from collections import OrderedDict

from lib.config import Config, CFG_FILE
from lib.color import *

def add_common_separators(wordlist):
    """
    Take a wordlist and generate all possible combinations between the words
    contained and another wordlist which contains common separator (e.g. _ ).

    :param wordlist: the base wordlist to combine
    :return: a new wordlist with all the combinations
    """

    if not Config.SEPARATORS_CHARSET:
        print('  {}[!]{} Any separators charset specified in {}'.format(color.ORANGE, color.END, CFG_FILE))

    words = wordlist[:]
    new_wordlist = []
    for word in words:
        for separator in Config.SEPARATORS_CHARSET:
            new_wordlist.append(word + separator)
            new_wordlist.append(separator + word)

    base_wordlist_with_seps = new_wordlist[:]

    for word in words:
        for wordseparated in base_wordlist_with_seps:
            if word not in wordseparated:
                new_wordlist.append(wordseparated + word)
                new_wordlist.append(word + wordseparated)

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

