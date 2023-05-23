#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - transform functions module

from multiprocessing.dummy import Pool as ThreadPool
from collections import OrderedDict

from . import Config

def compare(word_to_exclude, word_in_wordlist):
    if word_in_wordlist is not word_to_exclude:
        return word_in_wordlist

# Remove word to exclude from final_wordlist
def multithread_exclude(word_to_exclude, wordlist):
    diff_wordlist = []
    with ThreadPool(Config.THREADS) as pool:
        #args = (word, words_to_exclude)
        diff_wordlist += pool.starmap(compare, [(word_to_exclude, word) for word in wordlist])

    return [word for word in diff_wordlist if word is not None]

def remove_duplicates(wordlist):
    return list(OrderedDict.fromkeys(wordlist))

def remove_by_lengths(wordlist, min_length, max_length):
    '''expect a list, return a new list with the values between min and max length provided'''
    return [
        str(word)
        for word in wordlist
        if (len(str(word)) >= min_length) and (len(str(word)) <= max_length)
    ]