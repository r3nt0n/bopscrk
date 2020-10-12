#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - main script

"""
Before Outset PaSsword CRacKing is a tool to assist in the previous process of
cracking passwords. By now, it's able to generate smart and powerful wordlists.
"""

name =  'bopscrk.py'
__author__ = 'r3nt0n'
__version__ = '2.2'
__status__ = 'Development'


import os
import sys
import itertools
import argparse

from multiprocessing.dummy import Pool as ThreadPool

from lib.aux import *
from lib.banners import *     # inside import color
from lib.transforms import *  # inside import config
from lib.combinators import *


################################################################################
# ARGS DEFINITION
################################################################################
def read_args():
    parser = argparse.ArgumentParser(description='Generates smart and powerful wordlists.')

    parser.add_argument('-i', '--interactive', action="store_true",
                        help='interactive mode, the script will ask you about target')

    parser.add_argument('-w', action="store", metavar='', type=str, dest='words',
                        help='words (weight-1) to combine comma-separated (will be combined with all words)')

    # still to implement (next feature)
    # parser.add_argument('-w2', action="store", metavar='', type=str, dest='words',
    #                     help='words (weight-2) to combine comma-separated (will be combined with all weight-1 words)')

    parser.add_argument('-m', '--min', action="store", metavar='', type=int, dest='min',
                        default=4, help='min length for the words to generate (default: 4)')

    parser.add_argument('-M', '--max', action="store", metavar='', type=int, dest='max',
                        default=32, help='max length for the words to generate (default: 32)')

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
    #interactive = args.interactive
    if args.interactive:
        clear()
        bopscrk_banner()
        help_banner()
        banner(name, __version__, __author__)
        base_wordlist, minLength, maxLength, leet, case, nWords, artists, exclude_wordlists, outfile = asks()    #,ly_all_transforms

    else:
        bopscrk_banner()
        help_banner()
        banner(name, __version__, __author__)
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
    final_wordlist = base_wordlist[:]  # Copy to preserve the original


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
    # final_wordlist += add_common_separators(base_wordlist)


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
                final_wordlist += space_transforms(artist)

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
                    final_wordlist.append(phrase)

                # Make all possible transforms taking the song's phrases as base (leet, case and spaces)
                # if ly_all_transforms:
                # Add the raw phrases to main wordlist (leet and case transform will be performed on it later if its enabled)
                final_wordlist += lyrics
                # Make space transforms and add it too
                if space_replacement:
                    lyrics = thread_transforms(space_transforms, lyrics)
                for phrase in lyrics:
                    final_wordlist += phrase


    # WORD COMBINATIONS
    ############################################################################
    if nWords > 1:
        i = 1
        while i < nWords:
            i += 1
            final_wordlist += combinator(base_wordlist, i)

    print('  {}[+]{} Creating all posible combinations between words...'.format(color.BLUE, color.END))
    # WORD COMBINATIONS WITH COMMON SEPARATORS
    ############################################################################
    print('  {}[+]{} Creating extra combinations (separators charset in {}{}{})'.format(color.BLUE, color.END,color.CYAN,CFG_FILE,color.END))
    final_wordlist += add_common_separators(base_wordlist)


    # Check for duplicates
    final_wordlist = list(OrderedDict.fromkeys(final_wordlist))
    # Remove words which doesn't match the min-max range established
    final_wordlist = remove_by_lengths(final_wordlist, minLength, maxLength)


    # CASE TRANSFORMS
    ############################################################################
    if case:
        print('  {}[+]{} Applying case transforms...'.format(color.BLUE, color.END))
        thread_transforms(case_transforms, final_wordlist)

    # LEET TRANSFORMS
    ############################################################################
    if leet:
        if not LEET_CHARSET:
            print('  {}[!]{} Any leet charset specified in {}'.format(color.ORANGE, color.END, CFG_FILE))
            print('  {}[!]{} Skipping leet transforms...'.format(color.ORANGE, color.END, CFG_FILE))
        else:
            print('  {}[+]{} Applying leet transforms...'.format(color.BLUE, color.END))
            thread_transforms(leet_transforms, final_wordlist)

    # EXCLUDE FROM OTHER WORDLISTS
    ############################################################################
    if exclude_wordlists:
        print('  {}[+]{} Excluding wordlists...'.format(color.BLUE, color.END))
        words_to_exclude = []
        for wl_path in exclude_wordlists:
            with open(wl_path, 'r') as wlist_file:
                wl = wlist_file.read()
            wl = wl.split('\n')
            words_to_exclude += wl

        diff_wordlist = []
        with ThreadPool(16) as pool:
            #args = (word, words_to_exclude)
            diff_wordlist += pool.starmap(exclude, [(word, words_to_exclude) for word in final_wordlist])

        final_wordlist = [word for word in diff_wordlist if word is not None]
        # re-check by lengths
        final_wordlist = remove_by_lengths(final_wordlist, minLength, maxLength)

    # re-check for duplicates
    final_wordlist = list(OrderedDict.fromkeys(final_wordlist))


    # SAVE WORDLIST TO FILE
    ############################################################################
    with open(outfile, 'w') as f:
        for word in final_wordlist:
            f.write(word + '\n')

    # Final timestamps
    end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    total_time = (datetime.datetime.strptime(end_time, '%H:%M:%S') -
                  datetime.datetime.strptime(start_time, '%H:%M:%S'))

    # PRINT RESULTS
    ############################################################################
    print('\n  {}[+]{} Time elapsed:\t{}'.format(color.GREEN, color.END, total_time))
    print('  {}[+]{} Output file:\t{}{}{}{}'.format(color.GREEN, color.END, color.BOLD, color.BLUE, outfile, color.END))
    print('  {}[+]{} Words generated:\t{}{}{}\n'.format(color.GREEN, color.END, color.RED, len(final_wordlist), color.END))
    sys.exit(0)


################################################################################
################################################################################

if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt: print('\n\n  {}[!]{} Exiting...\n'.format(color.RED, color.END)); sys.exit(3)

