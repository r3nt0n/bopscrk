#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk

"""
Before Outset PaSsword CRacKing is a tool to assist in the previous process of
cracking passwords. By now, it's able to generate smart and powerful wordlists.
"""

global name, __author__,  __version__
name =  'bopscrk.py'
__author__ = 'r3nt0n'
__version__ = '2.2'
__status__ = 'Development'


import os
import sys
import datetime
import itertools
import argparse
import configparser
from time import sleep
from random import randint, choice
from collections import OrderedDict
from multiprocessing.dummy import Pool as ThreadPool



class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[33m'
    GREY = '\033[90m'
    #ORANGEBG = '\033[48;2;255;165;0m'
    END = '\033[0m'

    RAND_KEY_COLOR = [PURPLE, CYAN, DARKCYAN, YELLOW, ORANGE]
    KEY_HIGHL = choice(RAND_KEY_COLOR)



################################################################################
interval = 0.03

def banner():
    try:
        name_rand_leet = leet_transforms(name)
        name_rand_leet = name_rand_leet[randint(0, (len(name_rand_leet) - 1))]
    except:
        name_rand_leet = name
    name_rand_case = case_transforms(name)
    name_rand_case = name_rand_case[randint((len(name_rand_case) - 3), (len(name_rand_case) - 1))]

    print('  ,----------------------------------------------------,   ,------------,');sleep(interval)
    print('  | [][][][][]  [][][][][]  [][][][]  [][__]  [][][][] |   |    v{}{}{}    |'.format(color.BLUE, __version__, color.END));sleep(interval)
    print('  |                                                    |   |------------|');sleep(interval)
    print('  |  [][][][][][][][][][][][][][_]    [][][]  [][][][] |===| {}{}{} |'.format(color.RED, name_rand_leet, color.END));sleep(interval)
    print('  |  [_][][][]{}[]{}[][][][]{}[][]{}[][][ |   [][][]  [][][][] |===| {}{}{}{} |'.format(color.KEY_HIGHL, color.END, color.KEY_HIGHL, color.END, color.BOLD, color.RED, name, color.END));sleep(interval)
    print('  | [][_][]{}[]{}[][][][][]{}[]{}[][][][]||     []    [][][][] |===| {}{}{} |'.format(color.KEY_HIGHL, color.END, color.KEY_HIGHL, color.END, color.RED, name_rand_case, color.END));sleep(interval)
    print('  | [__][][][]{}[]{}[]{}[]{}[][][][][][__]    [][][]  [][][]|| |   |------------|'.format(color.KEY_HIGHL, color.END, color.KEY_HIGHL, color.END));sleep(interval)
    print('  |   [__][________________][__]              [__][]|| |   |{}   {}   {}|'.format(color.GREEN, __author__, color.END));sleep(interval)
    print('  `----------------------------------------------------´   `------------´\n');sleep(interval)

def help_banner():
    print(u'  +---------------------------------------------------------------------+');sleep(interval)
    print(u'  | Fields can be left empty.  You can use accentuation in your words.  |');sleep(interval)
    print(u'  | If you enable case transforms,  won\'t matter the lower/uppercases   |');sleep(interval)
    print(u'  | in your input. In "others" field (interactive mode), you can write  |');sleep(interval)
    print(u'  | several words comma-separated (e.g.: 2C,Flipper).                   |');sleep(interval)
    print(u'  |                                                                     |');sleep(interval)
    print(u'  |                              For advanced usage and documentation:  |');sleep(interval)
    print(u'  |                                  {}https://github.com/r3nt0n/bopscrk{}  |'.format(color.ORANGE,color.END));sleep(interval)
    print(u'  +---------------------------------------------------------------------+\n');sleep(interval)

def bopscrk_banner():
    sleep(interval * 4)
    print('\n')
    print(u'{}         ▄▄▄▄    ▒█████   ██▓███    ██████  ▄████▄   ██▀███   ██ ▄█▀'.format(color.ORANGE));sleep(interval)
    print(u'        ▓█████▄ ▒██▒  ██▒▓██░  ██▒▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒ ██▄█▒ ');sleep(interval)
    print(u'        ▒██▒ ▄██▒██░  ██▒▓██░ ██▓▒░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▓███▄░ ');sleep(interval)
    print(u'        ▒██░█▀  ▒██   ██░▒██▄█▓▒ ▒  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ▓██ █▄ ');sleep(interval)
    print(u'        ░▓█  ▀█▓░ ████▓▒░▒██▒ ░  ░▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒▒██▒ █▄');sleep(interval)
    print(u'        ░▒▓███▀▒░ ▒░▒░▒░ ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒');sleep(interval)
    print(u'        ▒░▒   ░   ░ ▒ ▒░ ░▒ ░     ░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░░ ░▒ ▒░');sleep(interval)
    print(u'         ░    ░ ░ ░ ░ ▒  ░░       ░  ░  ░  ░          ░░   ░ ░ ░░ ░');sleep(interval)
    print(u'         ░          ░ ░                 ░  ░ ░         ░     ░  ░');sleep(interval)
    print(u'              ░                            ░                        {}'.format(color.END));sleep(interval)
    #sleep(interval*2)

################################################################################
# ARGS DEFINITION
################################################################################
def read_args():
    parser = argparse.ArgumentParser(description='Generates smart and powerful wordlists.')

    parser.add_argument('-i', '--interactive', action="store_true",
                        help='interactive mode, the script will ask you about target')

    parser.add_argument('-w', action="store", metavar='', type=str, dest='words',
                        help='words to combine comma-separated (non-interactive mode)')

    parser.add_argument('--min', action="store", metavar='', type=int, dest='min',
                        default=4, help='min length for the words to generate '
                                        '(default: 4)')
    parser.add_argument('--max', action="store", metavar='', type=int, dest='max',
                        default=32, help='max length for the words to generate '
                                         '(default: 32)')
    parser.add_argument('-c', '--case', action="store_true", help='enable case transformations')

    parser.add_argument('-l', '--leet', action="store_true", help='enable leet transformations')

    parser.add_argument('-n', action="store", metavar='', type=int, dest='nWords',
                        default=2, help='max amount of words to combine each time '
                                        '(default: 2)')
    parser.add_argument('-a', '--artists', action="store", metavar='', type=str,
                        dest='artists', default=False,
                        help='artists to search song lyrics (comma-separated)')

    # parser.add_argument('-A', '--lyrics-all', action="store_true", default=False, dest='lyrics_all',
    #                     help='enable all possible transforms with lyrics')

    parser.add_argument('-x', '--exclude', action="store", metavar='', type=str,
                        dest='exclude', default=False,
                        help='exclude all the words included in other wordlists '
                             '(several wordlists should be comma-separated)')

    parser.add_argument('-o', '--output', action="store", metavar='', type=str,
                        dest='outfile', default='tmp.txt',
                        help='output file to save the wordlist (default: tmp.txt)')

    args = parser.parse_args()

    if len(sys.argv) == 1: bopscrk_banner(); help_banner(); parser.print_help(sys.stdout); sys.exit(2)  # Print simple help and exit when runs without args


    return args


# READING DEFAULT PARAMETERS FROM CONFIG FILE
###############################################################################
def read_conf(category, field):
    cfg = configparser.ConfigParser()
    try:
        cfg.read([CFG_FILE])
        value = cfg.get(category, field)
    except:
        value = False
    return value


# GLOBAL VARIABLES
###############################################################################
CFG_FILE = './bopscrk.cfg'
LEET_CHARSET = read_conf('TRANSFORMS', 'leet_charset')
# Reading spaces replacement charset from config file
space_replacement = []
space_replacement_chars = read_conf('TRANSFORMS', 'space_replacement_chars')
space_replacement_strings = read_conf('TRANSFORMS', 'space_replacement_strings')
if space_replacement_chars:
    space_replacement[:] = space_replacement_chars
if space_replacement_strings:
    space_replacement.extend(space_replacement_strings.split())
SPACE_REPLACEMENT = space_replacement


################################################################################
def clear():
    """Clear the screen. Works on Windows and Linux."""
    os.system(['clear', 'cls'][os.name == 'nt'])


################################################################################
def isEmpty(variable):
    """
    Check if a variable is empty.
    :param date_str: var to check
    :return: True or False
    """
    empty = False
    if len(str(variable)) == 0:
        empty = True
    return empty


################################################################################
def is_valid_date(date_str):
    """
    Check if a string corresponds to a valid date.
    :param date_str: date to check
    :return: True or False
    """
    try:
        datetime.datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False


################################################################################
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
    separators_chars = read_conf('COMBINATIONS', 'separators_chars')
    separators_strings = read_conf('COMBINATIONS', 'separators_strings')
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


################################################################################
def remove_by_lengths(wordlist, minLength, maxLength):
    new_wordlist = []
    for word in wordlist:
        #if (len(str(word)) < minLength) or (len(str(word)) > maxLength): wordlist.remove(word)
        if (len(str(word)) >= minLength) and (len(str(word)) <= maxLength): new_wordlist.append(str(word))
    return new_wordlist


################################################################################
def thread_transforms(transform_type, wordlist):
    pool = ThreadPool(16)
    # process each word in their own thread and return the results
    new_wordlist = pool.map(transform_type, wordlist)
    pool.close()
    pool.join()
    for lists in new_wordlist:
        wordlist += lists
    return new_wordlist


################################################################################
def space_transforms(word):
    new_wordlist = [word,]
    if ' ' in word:  # Avoiding non-space words to be included many times
        new_wordlist.append(word.replace(' ', ''))
        if space_replacement:
            for character in space_replacement:
                new_wordlist.append(word.replace(' ', character))

    return new_wordlist


################################################################################
def take_initials(word):
    splitted = word.split(' ')
    initials = ''
    for char in splitted:
        try: initials += char[0]
        except IndexError: continue
    return initials


################################################################################
def exclude(word):
    if word not in words_to_exclude:
        return word


################################################################################
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


################################################################################
def leet_transforms(word):
    new_wordlist = []
    i=0
    leet_charset = LEET_CHARSET.split()
    for char in word:
        for lchar in leet_charset:
            leeted_char = ''
            if lchar.startswith(char.lower()):
                leeted_char = lchar[-1:]
                new_word = word[:i] + leeted_char + word[i + 1:]
                if new_word not in new_wordlist: new_wordlist.append(new_word)
                # dont break to allow multiple transforms to a single char (e.g. a into 4 and @)
        i += 1

    # recursive call function
    recursive_leet = read_conf('TRANSFORMS', 'recursive_leet')
    if recursive_leet.lower() == 'true':
        for new_word in new_wordlist:
            original_size = len(new_wordlist)
            new_wordlist.extend(leet_transforms(new_word))
            if len(new_wordlist) == original_size:
                break  # breaking recursive call

    return new_wordlist


################################################################################
def asks():
    while True:
        minLength = input('  {}[?]{} Passwords min length [4] >>> '.format(color.BLUE, color.END))
        if isEmpty(minLength): minLength = 4; break
        else:
            try:
                minLength = int(minLength); break
            except ValueError:
                print('  {}[!]{} Min length should be an integer'.format(color.RED, color.END))
    while True:
        maxLength = input('  {}[?]{} Password\'s max length [32] >>> '.format(color.BLUE, color.END))
        if isEmpty(maxLength): maxLength = 32; break
        else:
            try:
                maxLength = int(maxLength)
                if maxLength < minLength: print('  {}[!]{} Max should be greater or equal than min'.format(color.RED, color.END))
                else: break
            except ValueError:
                print('  {}[!]{} Max length should be an integer'.format(color.RED, color.END))

    firstname = input('  {}[?]{} First name >>> '.format(color.BLUE, color.END))
    surname = input('  {}[?]{} Surname >>> '.format(color.BLUE, color.END))
    lastname = input('  {}[?]{} Last name >>> '.format(color.BLUE, color.END))

    while True:
        birth = input('  {}[?]{} Birth date (DD/MM/YYYY) >>> '.format(color.BLUE, color.END))
        if not isEmpty(birth) and not is_valid_date(birth):
            print('  {}[!]{} Birthdate wrong format'.format(color.RED, color.END))
        else:
            break

    others = input('  {}[?]{} Some other relevant words (comma-separated) >>> '.format(color.BLUE, color.END))

    leet = input('  {}[?]{} Do yo want to make leet transforms? [y/n] >>> '.format(color.BLUE, color.END))
    case = input('  {}[?]{} Do yo want to make case transforms? [y/n] >>> '.format(color.BLUE, color.END))

    if leet.lower() == 'y': leet = True
    else: leet = False

    if case.lower() == 'y': case = True
    else: case = False

    while True:
        nWords = input('  {}[?]{} How much words do you want to combine at most [2] >>> '.format(color.BLUE, color.END))
        if isEmpty(nWords): nWords = 2; break
        else:
            try:
                nWords = int(nWords)
                if nWords < 1:
                    print('  {}[!]{} Should be greater or equal than 1'.format(color.RED, color.END))
                else:
                    break
            except ValueError:
                print('  {}[!]{} Should be an integer'.format(color.RED, color.END))

    artists = input('  {}[?]{} Artist names to search song lyrics (comma-separated) >>> '.format(color.BLUE, color.END))
    if isEmpty(artists): artists = False
    # ly_all_transforms = False
    # if artists:
    #     ly_all_transforms = input('  {}[?]{} Do yo want to make all posible transforms with lyrics? (only huge wordlists) [y/n] >>> '.format(color.BLUE, color.END))
    #     if ly_all_transforms.lower() == 'y': ly_all_transforms = True

    while True:
        exclude = input('  {}[?]{} Exclude words from other wordlists? >>> '.format(color.BLUE, color.END))
        if isEmpty(exclude): exclude = False; break
        else:
            exclude = exclude.split(',')
            valid_paths = True
            for wl_path in exclude:
                if not os.path.isfile(wl_path):
                    valid_paths = False
                    print('  {}[!]{} {} not found'.format(color.RED, color.END, wl_path))
            if valid_paths:
                break

    outfile = input('  {}[?]{} Output file [tmp.txt] >>> '.format(color.BLUE, color.END))
    if isEmpty(outfile): outfile = 'tmp.txt'

    wordlist = []

    if not isEmpty(firstname):
        firstname = firstname.lower()
        wordlist.append(firstname)
    if not isEmpty(surname):
        surname = surname.lower()
        wordlist.append(surname)
    if not isEmpty(lastname):
        lastname = lastname.lower()
        wordlist.append(lastname)
    if not isEmpty(birth):
        birth = birth.split('/')
        for i in birth:
            wordlist.append(i)
        wordlist.append((birth[2])[-2:])  # Also add two last digits of the year
    if not isEmpty(others):
        others = others.split(',')
        for i in others:
            wordlist.append(i.lower())

    return wordlist, minLength, maxLength, leet, case, nWords, artists, exclude, outfile  #,ly_all_transforms


################################################################################
def main():
    # SETTINGS
    ############################################################################
    args = read_args()
    interactive = args.interactive
    if interactive:
        clear()
        bopscrk_banner()
        help_banner()
        banner()
        base_wordlist, minLength, maxLength, leet, case, nWords, artists, exclude_wordlists, outfile = asks()    #,ly_all_transforms

    else:
        bopscrk_banner()
        help_banner()
        banner()
        base_wordlist = []
        if args.words:
            raw_wordlist = (args.words).split(',')
            for word in raw_wordlist:
                base_wordlist.append(word.lower())
        minLength = args.min
        maxLength = args.max
        leet = args.leet
        case = args.case
        nWords = args.nWords
        artists = args.artists
        outfile = args.outfile
        #ly_all_transforms = args.lyrics_all

        exclude_wordlists = args.exclude
        if exclude_wordlists:
            exclude_wordlists = exclude_wordlists.split(',')
            for wl_path in exclude_wordlists:
                if not os.path.isfile(wl_path):
                    print('  {}[!]{} {} not found'.format(color.RED, color.END, wl_path))
                    sys.exit(4)
    if artists:
        artists = artists.split(',')

    # Initial timestamp
    start_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    wordlist = base_wordlist[:]  # Copy to preserve the original


    # # WORD COMBINATIONS
    # ############################################################################
    # if nWords > 1:
    #     wordlist = combinator(base_wordlist, 2)
    #     i = 2
    #     while i < nWords:
    #         i += 1
    #         wordlist += combinator(base_wordlist, i)
    #
    # print('  {}[+]{} Creating all posible combinations between words...'.format(color.BLUE, color.END))
    # # WORD COMBINATIONS WITH COMMON SEPARATORS
    # ############################################################################
    # print('  {}[+]{} Mixing, lpadding and rpadding words with separators (if any configured)...'.format(color.BLUE, color.END))
    # wordlist += add_common_separators(base_wordlist)


    # SEARCH FOR LYRICS
    ############################################################################
    if artists:
        try:
            from lib.lyricpass import lyricpass
            searchLyrics = True
            print('\n{}     -- Starting lyricpass module (by initstring) --\n'.format(color.GREY))
        except ImportError:
            print('  {}[!]{} missing dependencies, only artist names will be added and transformed'.format(color.RED, color.END))
            searchLyrics = False

        for artist in artists:
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # Add IN BASE WORDLIST artist name as a word  !!!!!!!!!!!! Start point created to implement weighted-words system !!!!!!!!!!!!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            base_wordlist.append(artist)
            # Add artist name with all space transformed into a specific charset
            if not SPACE_REPLACEMENT:
                print('  {}[!]{} Any spaces-replacement charset specified in {}'.format(color.ORANGE, color.END, CFG_FILE))
                print('  {}[!]{} Spaces inside artists names and lyrics phrases will be simply removed\n'.format(color.ORANGE, color.END))
            else:
                wordlist += space_transforms(artist)

            # Search lyrics if it meets dependencies for lyricpass
            if searchLyrics:
                print('  {}[*]{} Looking for {}\'s lyrics...'.format(color.CYAN, color.END, artist.title()))
                lyrics = lyricpass.lyricpass(artist)
                #lyrics = [s.decode("utf-8") for s in lyfinder.lyrics]
                print('\n  {}[*] {}{}{} phrases found\n'.format(color.CYAN, color.GREEN, len(lyrics), color.END))

                # First we remove all the parenthesis in the phrases
                lyrics = ([s.replace('(', '') for s in lyrics])
                lyrics = ([s.replace(')', '') for s in lyrics])

                # Now take just the initials on each phrase and add as a word
                base_lyrics = lyrics[:]
                ly_initials_wl = thread_transforms(take_initials, base_lyrics)
                for phrase in ly_initials_wl:
                    wordlist.append(phrase)

                # Make all possible transforms taking the song's phrases as base (leet, case and spaces)
                # if ly_all_transforms:
                # Add the raw phrases to main wordlist (leet and case transform will be performed on it later if its enabled)
                wordlist += lyrics
                # Make space transforms and add it too
                if space_replacement:
                    lyrics = thread_transforms(space_transforms, lyrics)
                for phrase in lyrics:
                    wordlist += phrase


    # WORD COMBINATIONS
    ############################################################################
    if nWords > 1:
        i = 2
        while i < nWords:
            i += 1
            wordlist += combinator(base_wordlist, i)

    print('  {}[+]{} Creating all posible combinations between words...'.format(color.BLUE, color.END))
    # WORD COMBINATIONS WITH COMMON SEPARATORS
    ############################################################################
    print('  {}[+]{} Creating extra combinations (separators charset in {}{}{})'.format(color.BLUE, color.END,color.CYAN,CFG_FILE,color.END))
    wordlist += add_common_separators(base_wordlist)


    # Check for duplicates
    wordlist = list(OrderedDict.fromkeys(wordlist))
    # Remove words which doesn't match the min-max range established
    wordlist = remove_by_lengths(wordlist, minLength, maxLength)


    # CASE TRANSFORMS
    ############################################################################
    if case:
        print('  {}[+]{} Applying case transforms...'.format(color.BLUE, color.END))
        thread_transforms(case_transforms, wordlist)

    # LEET TRANSFORMS
    ############################################################################
    if leet:
        if not LEET_CHARSET:
            print('  {}[!]{} Any leet charset specified in {}'.format(color.ORANGE, color.END, CFG_FILE))
            print('  {}[!]{} Skipping leet transforms...'.format(color.ORANGE, color.END, CFG_FILE))
        else:
            print('  {}[+]{} Applying leet transforms...'.format(color.BLUE, color.END))
            thread_transforms(leet_transforms, wordlist)

    # EXCLUDE FROM OTHER WORDLISTS
    ############################################################################
    if exclude_wordlists:
        print('  {}[+]{} Excluding wordlists...'.format(color.BLUE, color.END))
        global words_to_exclude
        words_to_exclude = []

        for wl_path in exclude_wordlists:
            with open(wl_path, 'rb') as wlist_file:
                wl = wlist_file.read()
            wl = wl.split('\n')
            words_to_exclude += wl

        pool = ThreadPool(16)
        final_wordlist = pool.map(exclude, wordlist)
        pool.close()
        pool.join()

        wordlist = [word for word in final_wordlist if word is not None]

    # Check for duplicates and re-check by lengths
    wordlist = list(OrderedDict.fromkeys(wordlist))
    wordlist = remove_by_lengths(wordlist, minLength, maxLength)    

    # SAVE WORDLIST TO FILE
    ############################################################################
    with open(outfile, 'w') as f:
        for word in wordlist:
            f.write(word + '\n')

    # Final timestamp
    end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    total_time = (datetime.datetime.strptime(end_time, '%H:%M:%S') -
                  datetime.datetime.strptime(start_time, '%H:%M:%S'))

    # PRINT RESULTS
    ############################################################################
    print('\n  {}[+]{} Time elapsed:\t{}'.format(color.GREEN, color.END, total_time))
    print('  {}[+]{} Output file:\t{}{}{}{}'.format(color.GREEN, color.END, color.BOLD, color.BLUE, outfile, color.END))
    print('  {}[+]{} Words generated:\t{}{}{}\n'.format(color.GREEN, color.END, color.RED, len(wordlist), color.END))
    sys.exit(0)


################################################################################
################################################################################

if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt: print('\n\n  {}[!]{} Exiting...\n'.format(color.RED, color.END)); sys.exit(3)

