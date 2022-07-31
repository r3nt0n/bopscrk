#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - transform functions module

from multiprocessing.dummy import Pool as ThreadPool

#from tqdm import tqdm
from alive_progress import alive_bar

from . import Config
from .excluders import remove_duplicates
from .auxiliars import append_wordlist_to_file


def case_transforms(word):
    new_wordlist = []

    # Make each one upper (hello => Hello, hEllo, heLlo, helLo, hellO)
    i=0
    for char in word:
        new_word = word[:i] + char.upper() + word[i+1:]
        i += 1
        if new_word not in new_wordlist: new_wordlist.append(new_word)

    # Make pairs upper (hello => HeLlO)
    i=0
    new_word = ''
    for char in word:
        if i % 2 == 0: new_word += char.upper()
        else: new_word += char
        i += 1
    if new_word not in new_wordlist: new_wordlist.append(new_word)

    # Make odds upper (hello => hElLo)
    i=0
    new_word = ''
    for char in word:
        if i % 2 != 0: new_word += char.upper()
        else: new_word += char
        i += 1
    if new_word not in new_wordlist: new_wordlist.append(new_word)

    # Make consonants upper (hello => HeLLo)
    vowels = 'aeiou'
    new_word = ''
    for char in word:
        if char.lower() not in vowels: new_word += char.upper()
        else: new_word += char
    if new_word not in new_wordlist: new_wordlist.append(new_word)

    # Make vowels upper (hello => hEllO)
    new_word = ''
    for char in word:
        if char.lower() in vowels: new_word += char.upper()
        else: new_word += char
    if new_word not in new_wordlist: new_wordlist.append(new_word)

    # recursive call function (not working, maybe this option won't be even useful)
    # for new_word in new_wordlist:
    #     original_size = len(new_wordlist)
    #     new_wordlist.extend(case_transforms(new_word))
    #     if len(new_wordlist) == original_size:
    #         break  # breaking recursive call

    return new_wordlist


def leet_transforms(word):
    new_wordlist = []
    original_size = len(new_wordlist)
    i=0
    leet_charset = Config.LEET_CHARSET
    for char in word:
        for lchar in leet_charset:
            leeted_char = ''
            if lchar.startswith(char.lower()):
                leeted_char = lchar[-1:]
                new_word = word[:i] + leeted_char + word[i + 1:]
                if new_word not in new_wordlist: new_wordlist.append(new_word)
                # dont break to allow multiple transforms to a single char (e.g. a into 4 and @)
        i += 1

    # MULTITHREAD RECURSIVE call function (doesn't seem efficient)
    # if Config.RECURSIVE_LEET and (len(new_wordlist) > original_size):
    #     new_wordlist += multithread_transforms(leet_transforms, new_wordlist)

    # UNITHREAD RECURSIVE call function
    if Config.RECURSIVE_LEET:
        for new_word in new_wordlist:
            original_size = len(new_wordlist)
            new_wordlist.extend(leet_transforms(new_word))
            if len(new_wordlist) == original_size:
                break  # breaking recursive call

    return remove_duplicates(new_wordlist)


def take_initials(word):
    splitted = word.split(' ')
    initials = ''
    for char in splitted:
        try: initials += char[0]
        except IndexError: continue
    return initials


def artist_space_transforms(word):
    new_wordlist = []
    if ' ' in word:  # Avoiding non-space words to be included many
        if Config.ARTIST_SPLIT_BY_WORD:
            # Add each word in the artist name splitting by spaces (e.g.: ['bob', 'dylan'])
            new_wordlist.extend(word.split(' '))
        # Add artist name without spaces (e.g.: 'bobdylan')
        new_wordlist.append(word.replace(' ', ''))
        # Replace spaces in artist name with all space replacements charset
        if (Config.ARTIST_SPACE_REPLACEMENT and Config.SPACE_REPLACEMENT_CHARSET):
            for character in Config.SPACE_REPLACEMENT_CHARSET:
                new_wordlist.append(word.replace(' ', character))

    return new_wordlist


def lyric_space_transforms(word):
    new_wordlist = []
    if ' ' in word:  # Avoiding non-space words to be included many
        if Config.LYRIC_SPLIT_BY_WORD:
            # Add each word in the phrase splitting by spaces (e.g.: ['hello', 'world'])
            new_wordlist.extend(word.split(' '))
        # Add phrase without spaces (e.g.: 'helloworld')
        new_wordlist.append(word.replace(' ', ''))
        # Replace spaces in phrase with all space replacements charset
        if (Config.LYRIC_SPACE_REPLACEMENT and Config.SPACE_REPLACEMENT_CHARSET):
            for character in Config.SPACE_REPLACEMENT_CHARSET:
                new_wordlist.append(word.replace(' ', character))
    return new_wordlist


def multithread_transforms(transform_type, wordlist):
    # process each word in their own thread and return the results
    new_wordlists = []
    with ThreadPool(Config.THREADS) as pool:
        with alive_bar(bar=None,spinner='bubbles', monitor=False,elapsed=False,stats=False,receipt=False) as progressbar:
            new_wordlists += pool.map(transform_type, wordlist)
            progressbar()
    new_wordlist = []
    for nlist in new_wordlists:
         new_wordlist += nlist
    return new_wordlist


def transform_cached_wordlist_and_save(transform_type, filepath):

    last_position = 0

    while True:

        cached_wordlist = []
        new_wordlist = []

        with open(filepath, 'r', encoding='utf-8') as f:
            counter = 0
            f.seek(last_position)  # put point on last position
            while True:
                line = f.readline()
                if counter >= 8000:
                    last_position = f.tell()  # save last_position and break inner loop
                    break
                if not line:
                    break
                if line.strip() not in cached_wordlist:
                    cached_wordlist.append(line.strip())
                counter += 1
                last_position = f.tell()  # save last_position

        new_wordlist += multithread_transforms(transform_type, cached_wordlist)
        #cached_wordlist += new_wordlist
        append_wordlist_to_file(filepath, new_wordlist)

        # read again the file to check if it ended
        with open(filepath, 'r', encoding='utf-8') as f:
            f.seek(last_position)  # put point on last position
            line = f.readline()
            if not line:
                break



