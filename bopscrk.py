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
__version__ = '2.2.6'
__status__ = 'Development'


import sys
#from collections import OrderedDict as ordDict
from lib.config import Config
from lib.args import Arguments
from lib.aux import *
from lib.banners import *     # inside import color
from lib.transforms import *
from lib.combinators import *
from lib.excluders import *


def main():
    # setting args
    args = Arguments()
    if args.interactive:
        clear()
        bopscrk_banner()
        help_banner()
        banner(name, __version__, __author__)
        args.set_interactive_options()
    else:
        bopscrk_banner()
        help_banner()
        banner(name, __version__, __author__)
        args.set_cli_options()

    # Initial timestamp
    start_time = datetime.datetime.now().time().strftime('%H:%M:%S')

    # Inserting original values into final_wordlist
    base_wordlist = args.base_wordlist
    final_wordlist = base_wordlist[:]  # Copy to preserve the original

    # WORD COMBINATIONS (?)

    # SEARCH FOR LYRICS
    if args.artists:
        for artist in args.artists:
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # Add IN BASE WORDLIST artist name as a word             !!!!
            # Start point created to implement weighted-words system !!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            base_wordlist.append(artist)
            # Add artist name with all space transformed into a specific charset
            if not Config.SPACE_REPLACEMENT_CHARSET:
                print('  {}[!]{} Any spaces-replacement charset specified in {}'.format(color.ORANGE, color.END, CFG_FILE))
                print('  {}[!]{} Spaces inside artists names and lyrics phrases will be simply removed\n'.format(color.ORANGE, color.END))
            else:
                final_wordlist += space_transforms(artist)

            # Search lyrics if it meets dependencies for lyricpass
            try:
                from lib.lyricpass import lyricpass
                print('\n{}     -- Starting lyricpass module (by initstring) --\n'.format(color.GREY))
                print('  {}[*]{} Looking for {}\'s lyrics...'.format(color.CYAN, color.END, artist.title()))
                lyrics = lyricpass.lyricpass(artist)
                #lyrics = [s.decode("utf-8") for s in lyfinder.lyrics]
                print('\n  {}[*] {}{}{} phrases found\n'.format(color.CYAN, color.GREEN, len(lyrics), color.END))

                # First we remove all the parenthesis in the phrases (if enabled)
                if Config.REMOVE_PARENTHESIS:
                    lyrics = ([s.replace('(', '') for s in lyrics])
                    lyrics = ([s.replace(')', '') for s in lyrics])

                # Add the phrases to main wordlist
                final_wordlist += lyrics

                # Take just the initials on each phrase and add as a new word
                if Config.TAKE_INITIALS:
                    base_lyrics = lyrics[:]
                    ly_initials_wl = multithread_transforms(take_initials, base_lyrics)
                    final_wordlist += ly_initials_wl

                # Make space transforms and add it too
                if Config.SPACE_REPLACEMENT_CHARSET:
                    space_transformed_lyrics = multithread_transforms(space_transforms, lyrics)
                    final_wordlist += space_transformed_lyrics

            except ImportError:
                print('  {}[!]{} missing dependencies, only artist names will be added and transformed'.format(color.RED, color.END))

    # WORD COMBINATIONS
    if args.n_words > 1:
        i = 1
        while i < args.n_words:
            i += 1
            final_wordlist += combinator(base_wordlist, i)

    print('  {}[+]{} Creating all posible combinations between words...'.format(color.BLUE, color.END))

    # WORD COMBINATIONS (WITH COMMON SEPARATORS)
    if Config.EXTRA_COMBINATIONS:
        print('  {}[+]{} Creating extra combinations (separators charset in {}{}{})'.format(color.BLUE, color.END,color.CYAN,CFG_FILE,color.END))
        final_wordlist += add_common_separators(base_wordlist)


    # Remove words by min-max length range established
    final_wordlist = remove_by_lengths(final_wordlist, args.min_length, args.max_length)
    # (!) Check for duplicates
    final_wordlist = list(OrderedDict.fromkeys(final_wordlist))


    # CASE TRANSFORMS
    if args.case:
        print('  {}[+]{} Applying case transforms...'.format(color.BLUE, color.END))
        multithread_transforms(case_transforms, final_wordlist)

    # LEET TRANSFORMS
    if args.leet:
        if not Config.LEET_CHARSET:
            print('  {}[!]{} Any leet charset specified in {}'.format(color.ORANGE, color.END, CFG_FILE))
            print('  {}[!]{} Skipping leet transforms...'.format(color.ORANGE, color.END, CFG_FILE))
        else:
            print('  {}[+]{} Applying leet transforms...'.format(color.BLUE, color.END))
            multithread_transforms(leet_transforms, final_wordlist)

    # EXCLUDE FROM OTHER WORDLISTS
    if args.exclude_wordlists:
        # For each path to wordlist provided
        for wl_path in args.exclude_wordlists:
            print('  {}[+]{} Excluding wordlist {}...'.format(color.BLUE, color.END, os.path.basename(wl_path)))
            # Open the file
            with open(wl_path, 'r') as x_wordlist_file:
                # Read line by line in a loop
                while True:
                    word_to_exclude = x_wordlist_file.readline()
                    if not word_to_exclude: break  # breaks the loop when file ends
                    final_wordlist = multithread_exclude(word_to_exclude, final_wordlist)

        # re-check by lengths
        #final_wordlist = remove_by_lengths(final_wordlist, min_length, max_length)

        # OLD APPROACH - This is not memory efficient and could crash handling large files
        # words_to_exclude = []
        # for wl_path in exclude_wordlists:
        #     with open(wl_path, 'r') as wlist_file:
        #         wlist = wlist_file.readlines()
        #     wl = wl.split('\n')
        #     words_to_exclude += wl
        #
        # diff_wordlist = []
        # with ThreadPool(16) as pool:
        #     #args = (word, words_to_exclude)
        #     diff_wordlist += pool.starmap(exclude, [(word, words_to_exclude) for word in final_wordlist])
        #
        # final_wordlist = [word for word in diff_wordlist if word is not None]
        # # re-check by lengths
        # final_wordlist = remove_by_lengths(final_wordlist, min_length, max_length)

    # re-check for duplicates
    final_wordlist = list(OrderedDict.fromkeys(final_wordlist))


    # SAVE WORDLIST TO FILE
    ############################################################################
    with open(args.outfile, 'w') as f:
        for word in final_wordlist:
            f.write(word + '\n')

    # Final timestamps
    end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    total_time = (datetime.datetime.strptime(end_time, '%H:%M:%S') -
                  datetime.datetime.strptime(start_time, '%H:%M:%S'))

    # PRINT RESULTS
    ############################################################################
    print('\n  {}[+]{} Time elapsed:\t{}'.format(color.GREEN, color.END, total_time))
    print('  {}[+]{} Output file:\t{}{}{}{}'.format(color.GREEN, color.END, color.BOLD, color.BLUE, args.outfile, color.END))
    print('  {}[+]{} Words generated:\t{}{}{}\n'.format(color.GREEN, color.END, color.RED, len(final_wordlist), color.END))
    sys.exit(0)



if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt: print('\n\n  {}[!]{} Exiting...\n'.format(color.RED, color.END)); sys.exit(3)

