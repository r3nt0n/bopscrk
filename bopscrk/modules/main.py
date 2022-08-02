#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - script opts and presentation

import sys, os, datetime

#from bopscrk.bopscrk import name, __version__, __author__
from . import args, Config
from .auxiliars import clear, remove_duplicates_from_file
from . import banners
from .color import color
from .transforms import leet_transforms, case_transforms, artist_space_transforms, lyric_space_transforms, multithread_transforms, take_initials, transform_cached_wordlist_and_save
from .combinators import combinator, add_common_separators
from .excluders import remove_by_lengths, remove_duplicates, multithread_exclude


def run(name, version):
    # check Python version
    if sys.version_info < (3, 0): print('Python 3 is required'); sys.exit(1)
    # Print simple help and exit when runs without args
    if len(sys.argv) == 1: args.parser.print_help(sys.stdout); sys.exit(2)
    # Print version and exit (when runs with -v)
    if args.print_version: print(name + '_' + version); sys.exit(0)

    try:
        # setting args whter interactive or not
        if args.interactive:
            clear()
            banners.bopscrk_banner()
            banners.help_banner()
            banners.banner(name, version)
            args.set_interactive_options()
        else:
            banners.bopscrk_banner()
            banners.help_banner()
            banners.banner(name, version)
            args.set_cli_options()

        # Check if config file exists
        if not os.path.exists(args.cfg_file):
            print('  {}[!]{} error trying to load config file {}'.format(color.RED, color.END, args.cfg_file))
            sys.exit(3)

        else:
            Config.setup()
            print('  {}[V]{} config file {} loaded'.format(color.GREEN, color.END, args.cfg_file))

        # Initial timestamp
        start_time = datetime.datetime.now().time().strftime('%H:%M:%S')

        # Inserting original values into final_wordlist
        base_wordlist = args.base_wordlist
        print('  {}[+]{} Appending words provided (base wordlist length: {})...'.format(color.BLUE, color.END, len(base_wordlist)))
        final_wordlist = base_wordlist[:]  # Copy to preserve the original

        # SEARCH FOR LYRICS
        if args.artists:
            print('  {}[+]{} Appending artist names   (base wordlist length: {})...'.format(color.BLUE, color.END,(len(base_wordlist)+len(args.artists))))
            for artist in args.artists:
                # Add IN BASE WORDLIST artist name as a word
                base_wordlist.append(artist)

                # Add artist name with all space transformed configured (and enabled) into a specific charset
                if not (Config.SPACE_REPLACEMENT_CHARSET and Config.ARTIST_SPACE_REPLACEMENT):
                    print('  {}[!]{} Any space-replacement charset specified in {}'.format(color.ORANGE, color.END, args.cfg_file))
                    print('  {}[!]{} Spaces inside artists names won\'t be replaced\n'.format(color.ORANGE, color.END))
                elif Config.ARTIST_SPACE_REPLACEMENT:
                    print('  {}[+]{} Producing new words replacing any space in {}...'.format(color.BLUE, color.END,artist))
                    final_wordlist += artist_space_transforms(artist)

                # Search lyrics if it meets dependencies for lyricpass
                try:
                    from .lyricpass import lyricpass
                    print('\n{}     -- Starting lyricpass module --\n'.format(color.GREY))
                    print('  {}[*]{} Looking for {}\'s lyrics...'.format(color.CYAN, color.END, artist.title()))
                    lyrics = lyricpass.lyricpass(artist)
                    #lyrics = [s.decode("utf-8") for s in lyfinder.lyrics]
                    print('\n  {}[*] {}{}{} phrases found'.format(color.CYAN, color.GREEN, len(lyrics), color.END))
                    print('\n{}     -- Stopping lyricpass module --\n'.format(color.GREY))

                    # First we remove all the parenthesis in the phrases (if enabled)
                    if Config.REMOVE_PARENTHESIS:
                        lyrics = ([s.replace('(', '') for s in lyrics])
                        lyrics = ([s.replace(')', '') for s in lyrics])

                    # Add the phrases to BASE wordlist
                    lyrics = remove_by_lengths(lyrics, args.min_length, args.max_length)
                    print('  {}[+]{} Adding raw phrases filtering by min and max length range ({} phrases remain)...'.format(color.BLUE, color.END,len(lyrics)))
                    final_wordlist += lyrics

                    # Take just the initials on each phrase and add as a new word to FINAL wordlist
                    if Config.TAKE_INITIALS:
                        base_lyrics = lyrics[:]
                        ly_initials_wordlist = multithread_transforms(take_initials, base_lyrics)
                        final_wordlist += ly_initials_wordlist

                    # Make space transforms and add it too
                    if not (Config.SPACE_REPLACEMENT_CHARSET and Config.LYRIC_SPACE_REPLACEMENT):
                        print('  {}[!]{} Any spaces-replacement charset specified in {}'.format(color.ORANGE, color.END, args.cfg_file))
                        print('  {}[!]{} Spaces inside lyrics won\'t be replaced\n'.format(color.ORANGE,color.END))
                    elif Config.LYRIC_SPACE_REPLACEMENT:
                        print('  {}[+]{} Producing new words replacing spaces in {} phrases...'.format(color.BLUE, color.END, len(lyrics)))
                        base_lyrics = lyrics[:]
                        space_transformed_lyrics = multithread_transforms(lyric_space_transforms, base_lyrics)
                        final_wordlist += space_transformed_lyrics

                except ImportError:
                    print('  {}[!]{} missing dependencies, only artist names will be added and transformed'.format(color.RED, color.END))

        # WORD COMBINATIONS
        if ((args.n_words > 1)):
            print('  {}[+]{} Creating all posible combinations between words...'.format(color.BLUE, color.END))
            i = 1
            while ((i < args.n_words) and (len(base_wordlist) > i)):
                i += 1
                final_wordlist += combinator(base_wordlist, i)
                print('  {}[*]{} {} words combined using {} words (words produced: {})'.format(color.CYAN,color.END,len(base_wordlist),i, len(final_wordlist)))

        # WORD COMBINATIONS (WITH COMMON SEPARATORS)
        if Config.EXTRA_COMBINATIONS:
            if Config.SEPARATORS_CHARSET:
                #print('  {}[+]{} Creating extra combinations (separators charset in {}{}{})...'.format(color.BLUE, color.END,color.CYAN, args.cfg_file,color.END))
                print('  {}[+]{} Creating extra combinations with separators charset...'.format(color.BLUE,color.END))
                final_wordlist += add_common_separators(base_wordlist)
                print('  {}[*]{} Words produced: {}'.format(color.CYAN, color.END, len(final_wordlist)))
            else:
                print('  {}[!]{} Any separators charset specified in {}{}'.format(color.ORANGE, color.END, args.cfg_file,color.END))

        # Remove words by min-max length range established
        print('  {}[-]{} Removing words by min and max length provided ({}-{})...'.format(color.PURPLE, color.END,args.min_length,args.max_length))
        final_wordlist = remove_by_lengths(final_wordlist, args.min_length, args.max_length)
        print('  {}[*]{} Words remained: {}'.format(color.CYAN, color.END, len(final_wordlist)))
        # (!) Check for duplicates (is checked before return in combinator() and add_common_separators())
        #final_wordlist = remove_duplicates(final_wordlist)


        # # CASE TRANSFORMS
        # if args.case:
        #     print('  {}[+]{} Applying case transforms to {} words...'.format(color.BLUE, color.END, len(final_wordlist)))
        #
        #     # transform_cached_wordlist_and_save(case_transforms, args.outfile) # not working yet, infinite loop ?¿?¿
        #     temp_wordlist = []
        #     temp_wordlist += multithread_transforms(case_transforms, final_wordlist)
        #     final_wordlist += temp_wordlist
        #
        # final_wordlist = remove_duplicates(final_wordlist)
        #
        # # SAVE WORDLIST TO FILE BEFORE LEET TRANSFORMS
        # ############################################################################
        # with open(args.outfile, 'w') as f:
        #     for word in final_wordlist:
        #         f.write(word + '\n')

        # LEET TRANSFORMS
        if args.leet:
            if not Config.LEET_CHARSET:
                print('  {}[!]{} Any leet charset specified in {}'.format(color.ORANGE, color.END, args.cfg_file))
                print('  {}[!]{} Skipping leet transforms...'.format(color.ORANGE, color.END, args.cfg_file))
            else:
                recursive_msg = ''
                if Config.RECURSIVE_LEET:
                    # print('\n  {}[!] WARNING: Recursive leet is enabled, depending on the words\n'
                    #       '      max-length configured (now is {}{}{}) and the size of your\n'
                    #       '      wordlist at this point (now contains {}{}{} words), this process\n'
                    #       '      could take a long time{}\n'.format(color.ORANGE,color.END,args.max_length,color.ORANGE,color.END,len(final_wordlist),color.ORANGE,color.END))
                    recursive_msg = '{}recursive{} '.format(color.RED,color.END)
                print('  {}[+]{} Applying {}leet transforms to {} words...'.format(color.BLUE, color.END, recursive_msg,len(final_wordlist)))

                #transform_cached_wordlist_and_save(leet_transforms, args.outfile)
                #remove_duplicates_from_file(args.outfile)

                temp_wordlist = []
                temp_wordlist += multithread_transforms(leet_transforms, final_wordlist)
                final_wordlist += temp_wordlist

        # CASE TRANSFORMS
        if args.case:
            print('  {}[+]{} Applying case transforms to {} words...'.format(color.BLUE, color.END,len(final_wordlist)))

            # transform_cached_wordlist_and_save(case_transforms, args.outfile) # not working yet, infinite loop ?¿?¿

            temp_wordlist = []
            temp_wordlist += multithread_transforms(case_transforms, final_wordlist)
            final_wordlist += temp_wordlist

        print('  {}[-]{} Removing duplicates...'.format(color.PURPLE, color.END))
        final_wordlist = remove_duplicates(final_wordlist)
        print('  {}[*]{} Words remained: {}'.format(color.CYAN, color.END, len(final_wordlist)))

        # EXCLUDE FROM OTHER WORDLISTS
        #if args.exclude_wordlists:
            # For each path to wordlist provided
            # for wl_path in args.exclude_wordlists:
            #     print('  {}[+]{} Excluding wordlist {}...'.format(color.BLUE, color.END, os.path.basename(wl_path)))
            #     # Open the file
            #     with open(wl_path, 'r') as x_wordlist_file:
            #         # Read line by line in a loop
            #         while True:
            #             word_to_exclude = x_wordlist_file.readline()
            #             if not word_to_exclude: break  # breaks the loop when file ends
            #             final_wordlist = multithread_exclude(word_to_exclude, final_wordlist)

        # re-check for duplicates
        #final_wordlist = remove_duplicates(final_wordlist)

        # SAVE WORDLIST TO FILE
        ###########################################################################
        with open(args.outfile, 'w') as f:
            for word in final_wordlist:
                f.write(word + '\n')

        # Final timestamps
        end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        total_time = (datetime.datetime.strptime(end_time, '%H:%M:%S') -
                      datetime.datetime.strptime(start_time, '%H:%M:%S'))

        # PRINT RESULTS
        ############################################################################
        print('\n  {}[+]{} Words generated:\t{}{}{}'.format(color.GREEN, color.END, color.RED, len(final_wordlist),color.END))
        print('  {}[+]{} Time elapsed:\t{}'.format(color.GREEN, color.END, total_time))
        print('  {}[+]{} Output file:\t{}{}{}{}'.format(color.GREEN, color.END, color.BOLD, color.BLUE, args.outfile, color.END))
        #print('  {}[+]{} Words generated:\t{}{}{}\n'.format(color.GREEN, color.END, color.RED, str(sum(1 for line in open(args.outfile))), color.END))
        sys.exit(0)

    except KeyboardInterrupt:
        print('\n\n  {}[!]{} Exiting...\n'.format(color.RED, color.END))
        sys.exit(3)
