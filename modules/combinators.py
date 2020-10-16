#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - combinators functions module

import itertools

from bopscrk import Config
from modules.excluders import remove_duplicates


def add_common_separators(wordlist):
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

    return remove_duplicates(new_wordlist)


def combinator(wordlist, nWords):
    new_wordlist = wordlist[:]  # I need copy to use itertools properly
    wlist_combined = itertools.permutations(new_wordlist, nWords)
    for combination in wlist_combined:
        word = ''
        for i in combination:
            word += i
        if word not in new_wordlist: new_wordlist.append(word)

    return remove_duplicates(new_wordlist)

