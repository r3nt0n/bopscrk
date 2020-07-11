#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n 25/10/2017
# last update: 17/06/2020

"""
Before Outset PaSsword CRacKing is a tool to assist in the previous process of
cracking passwords. By now, it's able to generate smart and powerful wordlists.
"""

global name, __author__,  __version__
name =  'bopscrk.py'
__author__ = 'r3nt0n'
__version__ = '2.0'
__status__ = 'Development'



import os
import sys
import datetime
import itertools
import argparse
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
    #ORANGEBG = '\033[48;2;255;165;0m'
    END = '\033[0m'

    RAND_KEY_COLOR = [PURPLE, CYAN, DARKCYAN, YELLOW, ORANGE]
    KEY_HIGHL = choice(RAND_KEY_COLOR)


################################################################################
# ARGS DEFINITION
################################################################################
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

parser.add_argument('-A', '--lyrics-all', action="store_true", default=False, dest='lyrics_all',
                    help='enable all possible transforms with lyrics')

parser.add_argument('-x', '--exclude', action="store", metavar='', type=str,
                    dest='exclude', default=False,
                    help='exclude all the words included in other wordlists '
                         '(several wordlists should be comma-separated)')

parser.add_argument('-o', '--output', action="store", metavar='', type=str,
                    dest='outfile', default='tmp.txt',
                    help='output file to save the wordlist (default: tmp.txt)')


################################################################################
def banner():
    name_rand_leet = leet_transforms(name)
    name_rand_leet = name_rand_leet[randint(0, (len(name_rand_leet) - 1))]
    name_rand_case = case_transforms(name)
    name_rand_case = name_rand_case[randint((len(name_rand_case) - 3), (len(name_rand_case) - 1))]

    print('\n  ,----------------------------------------------------,   ,------------,')
    print('  | [][][][][]  [][][][][]  [][][][]  [][__]  [][][][] |   |    v{}{}{}    |'.format(color.BLUE, __version__, color.END))
    print('  |                                                    |   |------------|')
    print('  |  [][][][][][][][][][][][][][_]    [][][]  [][][][] |===| {}{}{} |'.format(color.RED, name_rand_leet, color.END))
    print('  |  [_][][][]{}[]{}[][][][]{}[][]{}[][][ |   [][][]  [][][][] |===| {}{}{}{} |'.format(color.KEY_HIGHL, color.END, color.KEY_HIGHL, color.END, color.BOLD, color.RED, name, color.END))
    print('  | [][_][]{}[]{}[][][][][]{}[]{}[][][][]||     []    [][][][] |===| {}{}{} |'.format(color.KEY_HIGHL, color.END, color.KEY_HIGHL, color.END, color.RED, name_rand_case, color.END))
    print('  | [__][][][]{}[]{}[]{}[]{}[][][][][][__]    [][][]  [][][]|| |   |------------|'.format(color.KEY_HIGHL, color.END, color.KEY_HIGHL, color.END))
    print('  |   [__][________________][__]              [__][]|| |   |{}   {}   {}|'.format(color.GREEN, __author__, color.END))
    print('  `----------------------------------------------------´   `------------´\n')
    # print u'  +--------------------------------------------------------------------+'
    # print u'  | Names have to be written without accents, just normal characters.  |'
    # print u'  | If you enable case transforms, doesn\'t matter the lower/uppercases |'
    # print u'  | in your input.                                                     |'
    # print u'  |                                                                    |'
    # print u'  | In the others field you can write several words comma-separated.   |'
    # print u'  | Example: 2C,Flipper                                                |'
    # print u'  |                                                                    |'
    # print u'  | Fields can be left empty.                                          |'
    # print u'  +--------------------------------------------------------------------+\n'


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
    common_separators = ['.', '_', '-', '123', '$', '%', '&', '#', '@']
    words = wordlist[:]
    new_wordlist = []

    for word in words:
        for sep in common_separators:
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
    new_wordlist = []
    new_wordlist.append(word.replace(' ', ''))
    new_wordlist.append(word.replace(' ', '.'))
    new_wordlist.append(word.replace(' ', '_'))
    new_wordlist.append(word.replace(' ', '-'))
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
        if char not in vowels: new_word += char.upper()
        else: new_word += char
    if new_word not in new_wordlist: new_wordlist.append(new_word)

    # Make vowels upper (hello => hEllO)
    new_word = ''
    for char in word:
        if char in vowels: new_word += char.upper()
        else: new_word += char
    if new_word not in new_wordlist: new_wordlist.append(new_word)

    return new_wordlist


################################################################################
def leet_transforms(word):
    new_wordlist = []
    i=0
    for char in word:
        if char in ('a', 'A'):
            char = '4'
        elif char in ('i', 'I'):
            char = '1'
        elif char in ('e', 'E'):
            char = '3'
        elif char in ('s', 'S'):
            char = '5'
        elif char in ('b', 'B'):
            char = '8'
        elif char in ('o', 'O'):
            char = '0'
        word = word[:i] + char + word[i + 1:]
        i += 1
        if word not in new_wordlist: new_wordlist.append(word)
    return new_wordlist


################################################################################
def asks():
    while True:
        minLength = input('  {}[?]{} Password\'s min length [1] >>> '.format(color.BLUE, color.END))
        if isEmpty(minLength): minLength = 1; break
        else:
            try:
                minLength = int(minLength); break
            except ValueError:
                print('  {}[!]{} Min length should be an integer'.format(color.RED, color.END))
    while True:
        maxLength = input('  {}[?]{} Password\'s max length [99] >>> '.format(color.BLUE, color.END))
        if isEmpty(maxLength): maxLength = 99; break
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

    ly_all_transforms = input('  {}[?]{} Do yo want to make all posible transforms with lyrics? (not recommended) [y/n] >>> '.format(color.BLUE, color.END))
    if ly_all_transforms.lower() == 'y': ly_all_transforms = True
    else: ly_all_transforms = False

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

    return wordlist, minLength, maxLength, leet, case, nWords, artists, ly_all_transforms, exclude, outfile


################################################################################
def main():
    args = parser.parse_args()
    interactive = args.interactive
    if len(sys.argv) == 1: parser.print_help(sys.stdout); sys.exit(2)  # Print help and exit when runs without args


    # SETTINGS
    ############################################################################
    if interactive:
        clear()
        banner()
        base_wordlist, minLength, maxLength, leet, case, nWords, artists, ly_all_transforms, exclude_wordlists, outfile = asks()

    else:
        base_wordlist = []
        if args.words:
            raw_wordlist = (args.words).split(',')
            for word in raw_wordlist:
                base_wordlist.append(word.lower())
        minLength = args.min
        maxLength = args.max
        case = args.case
        leet = args.leet
        nWords = args.nWords
        artists = args.artists
        outfile = args.outfile
        ly_all_transforms = args.lyrics_all

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


    # WORD COMBINATIONS
    ############################################################################
    if nWords > 1:
        wordlist = combinator(base_wordlist, 2)
        i = 2
        while i < nWords:
            i += 1
            wordlist += combinator(base_wordlist, i)

    # WORD COMBINATIONS WITH COMMON SEPARATORS
    ############################################################################
    wordlist += add_common_separators(base_wordlist)


    # SEARCH FOR LYRICS
    ############################################################################
    if artists:
        try:
            from lib.lyricpass import LyricsFinder
            searchLyrics = True
        except ImportError:
            print('  {}[!]{} missing dependencies, only artist names will be added and transformed'.format(color.RED, color.END))
            searchLyrics = False

        for artist in artists:
            wordlist.append(artist)
            wordlist += space_transforms(artist)

            if searchLyrics:
                print('  {}[*]{} Looking for {}\'s lyrics...'.format(color.CYAN, color.END, artist.title()))
                lyfinder = LyricsFinder(artist, False, True)
                lyrics = [s.decode("utf-8") for s in lyfinder.lyrics]
                print('  {}[*] {}{}{} phrases found'.format(color.CYAN, color.GREEN, len(lyrics), color.END))

                # First we remove all the parenthesis in the phrases
                lyrics = ([s.replace('(', '') for s in lyrics])
                lyrics = ([s.replace(')', '') for s in lyrics])

                # Now take just the initials
                base_lyrics = lyrics[:]
                ly_initials_wl = thread_transforms(take_initials, base_lyrics)
                for phrase in ly_initials_wl:
                    wordlist.append(phrase)

                # Make all possible transforms taking the song's phrases as base (leet, case and spaces)
                if ly_all_transforms:
                    # Add the raw phrases to main wordlist
                    wordlist += lyrics
                    # Make space transforms and add it too
                    lyrics = thread_transforms(space_transforms, lyrics)
                    for phrase in lyrics:
                        wordlist += phrase


    # Check for duplicates
    wordlist = list(OrderedDict.fromkeys(wordlist))
    # Remove words which doesn't match the min-max range established
    wordlist = remove_by_lengths(wordlist, minLength, maxLength)


    # UPPER/LOWER TRANSFORMS
    ############################################################################
    if case:
        thread_transforms(case_transforms, wordlist)


    # LEET TRANSFORMS
    ############################################################################
    if leet:
        thread_transforms(leet_transforms, wordlist)


    # EXCLUDE FROM OTHER WORDLISTS
    ############################################################################
    if exclude_wordlists:
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

