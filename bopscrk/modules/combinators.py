#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - combinators functions module

import itertools

#from tqdm import tqdm
from alive_progress import alive_bar

from . import Config
from .excluders import remove_duplicates


def add_common_separators(wordlist):
    words = wordlist[:]
    new_wordlist = []
    for word in words:
        for separator in Config.SEPARATORS_CHARSET:
            new_wordlist.append(word + separator)
            new_wordlist.append(separator + word)

    base_wordlist_with_seps = new_wordlist[:]

    #with tqdm(total=len(words)) as progressbar:
    with alive_bar(total=len(words),bar='bubbles',unknown='bubbles',spinner='bubbles',receipt=False) as progressbar:
        for word in words:
            for wordseparated in base_wordlist_with_seps:
                if word not in wordseparated:
                    new_wordlist.append(wordseparated + word)
                    new_wordlist.append(word + wordseparated)
            #progressbar.update()
            progressbar()

    return remove_duplicates(new_wordlist)


def combinator(wordlist, nWords):
    new_wordlist = wordlist[:]  # I need copy to use itertools properly
    wlist_combined = itertools.permutations(new_wordlist, nWords)
    #list_combined_length = (sum(1 for _ in wlist_combined))
    wlist_combined = [''.join(i) for i in wlist_combined]

    #with tqdm(total=len(wlist_combined)) as progressbar:
    with alive_bar(total=len(wlist_combined), bar='bubbles', unknown='bubbles', spinner='bubbles',receipt=False) as progressbar:
        for combination in wlist_combined:
            #progressbar.set_description("Processing %s" % combination)
            word = ''
            for i in combination:
                word += i
            if word not in new_wordlist: new_wordlist.append(word)
            #progressbar.update()
            progressbar()

    return remove_duplicates(new_wordlist)

