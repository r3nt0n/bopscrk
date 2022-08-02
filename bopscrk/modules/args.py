#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import os, sys, argparse

from .color import color
from .auxiliars import is_empty, is_valid_date


class Arguments:
    def __init__(self):
        self.DEFAULT_MIN = 4
        self.DEFAULT_MAX = 12
        self.DEFAULT_N_WORDS = 2
        self.DEFAULT_OUTPUT_FILE = 'tmp.txt'
        # scratch, still need to be regorganized
        import os
        self.DEFAULT_CFG_FILE = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '../bopscrk.cfg')
        )
        #self.DEFAULT_CFG_FILE = './bopscrk.cfg'

        parser = argparse.ArgumentParser(description='Generates smart and powerful wordlists.')

        parser.add_argument('-i', '--interactive', action="store_true",
                            help='interactive mode, the script will ask you about target')

        parser.add_argument('-w', action="store", metavar='', type=str, dest='words',
                            help='words to combine comma-separated (will be combined with all words)')

        parser.add_argument('-m', '--min', action="store", metavar='', type=int, dest='min',
                            default=self.DEFAULT_MIN, help='min length for the words to generate (default: {})'.format(self.DEFAULT_MIN))

        parser.add_argument('-M', '--max', action="store", metavar='', type=int, dest='max',
                            default=self.DEFAULT_MAX, help='max length for the words to generate (default: {})'.format(self.DEFAULT_MAX))

        parser.add_argument('-c', '--case', action="store_true", help='enable case transformations')

        parser.add_argument('-l', '--leet', action="store_true", help='enable leet transformations')

        parser.add_argument('-n', action="store", metavar='', type=int, dest='n_words',
                            default=self.DEFAULT_N_WORDS, help='max amount of words to combine each time '
                                            '(default: {})'.format(self.DEFAULT_N_WORDS))
        parser.add_argument('-a', '--artists', action="store", metavar='', type=str,
                            dest='artists', default=False,
                            help='artists to search song lyrics (comma-separated)')

        # parser.add_argument('-x', '--exclude', action="store", metavar='', type=str,
        #                     dest='exclude', default=False,
        #                     help='exclude all the words included in other wordlists '
        #                          '(several wordlists should be comma-separated)')

        parser.add_argument('-o', '--output', action="store", metavar='', type=str,
                            dest='outfile', default=self.DEFAULT_OUTPUT_FILE,
                            help='output file to save the wordlist (default: {})'.format(self.DEFAULT_OUTPUT_FILE))

        parser.add_argument('-C', '--config', action="store", metavar='', type=str,
                            dest='cfg_file', default=self.DEFAULT_CFG_FILE,
                            help='specify config file to use (default: {})'.format(self.DEFAULT_CFG_FILE))

        parser.add_argument('--version', action="store_true", help='print version and exit')

        self.parser = parser
        self.args = parser.parse_args()
        self.interactive = self.args.interactive
        self.cfg_file = self.args.cfg_file
        self.print_version = self.args.version

    def set_interactive_options(self):
        while True:
            min_length = input('  {}[?]{} Passwords min length [{}] >>> '.format(color.BLUE, color.END, self.DEFAULT_MIN))
            if is_empty(min_length):
                self.min_length = self.DEFAULT_MIN; break
            else:
                try:
                    self.min_length = int(min_length)
                    break
                except ValueError:
                    print('  {}[!]{} Min length should be an integer'.format(color.RED, color.END))
        while True:
            max_length = input('  {}[?]{} Password\'s max length [{}] >>> '.format(color.BLUE, color.END, self.DEFAULT_MAX))
            if is_empty(max_length):
                self.max_length = self.DEFAULT_MAX; break
            else:
                try:
                    max_length = int(max_length)
                    if max_length < self.min_length:
                        print('  {}[!]{} Max should be greater or equal than min'.format(color.RED, color.END))
                    else:
                        self.max_length = max_length
                        break
                except ValueError:
                    print('  {}[!]{} Max length should be an integer'.format(color.RED, color.END))

        firstname = input('  {}[?]{} First name >>> '.format(color.BLUE, color.END))
        surname = input('  {}[?]{} Surname >>> '.format(color.BLUE, color.END))
        lastname = input('  {}[?]{} Last name >>> '.format(color.BLUE, color.END))

        while True:
            birth = input('  {}[?]{} Birth date (DD/MM/YYYY) >>> '.format(color.BLUE, color.END))
            if not is_empty(birth) and not is_valid_date(birth):
                print('  {}[!]{} Birthdate wrong format'.format(color.RED, color.END))
            else:
                break

        self.artists = input('  {}[?]{} Artist names to search song lyrics (comma-separated) >>> '.format(color.BLUE, color.END))
        if is_empty(self.artists):
            self.artists = False
        else:
            self.artists = self.artists.split(',')

        others = input('  {}[?]{} Some other relevant words (comma-separated) >>> '.format(color.BLUE, color.END))

        leet = input('  {}[?]{} Do yo want to make leet transforms? [y/n] >>> '.format(color.BLUE, color.END))
        case = input('  {}[?]{} Do yo want to make case transforms? [y/n] >>> '.format(color.BLUE, color.END))

        if leet.lower() == 'y': self.leet = True
        else: self.leet = False

        if case.lower() == 'y': self.case = True
        else: self.case = False

        while True:
            n_words = input('  {}[?]{} How much words do you want to combine at most [{}] >>> '.format(color.BLUE, color.END, self.DEFAULT_N_WORDS))
            if is_empty(n_words):
                self.n_words = self.DEFAULT_N_WORDS; break
            else:
                try:
                    n_words = int(n_words)
                    if n_words < 1:
                        print('  {}[!]{} Should be greater or equal than 1'.format(color.RED, color.END))
                    else:
                        self.n_words = n_words
                        break
                except ValueError:
                    print('  {}[!]{} Should be an integer'.format(color.RED, color.END))

        # while True:
        #     exclude = input('  {}[?]{} Exclude words from other wordlists? >>> '.format(color.BLUE, color.END))
        #     if is_empty(exclude):
        #         self.exclude_wordlists = False; break
        #     else:
        #         exclude = exclude.split(',')
        #         valid_paths = True
        #         for wl_path in exclude:
        #             if not os.path.isfile(wl_path):
        #                 valid_paths = False
        #                 print('  {}[!]{} {} not found'.format(color.RED, color.END, wl_path))
        #         if valid_paths:
        #             self.exclude_wordlists = exclude
        #             break

        self.outfile = input('  {}[?]{} Output file [{}] >>> '.format(color.BLUE, color.END, self.DEFAULT_OUTPUT_FILE))
        if is_empty(self.outfile): self.outfile = self.DEFAULT_OUTPUT_FILE

        print('')  # Print blank line after all questions

        self.base_wordlist = []
        # here I can select on which wordlist include each info by their weight (to implement)
        if not is_empty(firstname):
            firstname = firstname.lower()
            self.base_wordlist.append(firstname)
        if not is_empty(surname):
            surname = surname.lower()
            self.base_wordlist.append(surname)
        if not is_empty(lastname):
            lastname = lastname.lower()
            self.base_wordlist.append(lastname)
        if not is_empty(birth):
            birth = birth.split('/')
            for i in birth:
                self.base_wordlist.append(i)
            self.base_wordlist.append((birth[2])[-2:])  # Also add two last digits of the year
        if not is_empty(others):
            others = others.split(',')
            for i in others:
                self.base_wordlist.append(i.lower())

    def set_cli_options(self):
        self.base_wordlist = []
        if self.args.words:
            [self.base_wordlist.append(word.lower()) for word in ((self.args.words).split(','))]
        self.min_length = self.args.min
        self.max_length = self.args.max
        self.leet = self.args.leet
        self.case = self.args.case
        self.n_words = self.args.n_words
        self.artists = self.args.artists
        self.outfile = self.args.outfile
        # self.exclude_wordlists = self.args.exclude
        # if self.exclude_wordlists:
        #     self.exclude_wordlists = self.exclude_wordlists.split(',')
        #     for wl_path in self.exclude_wordlists:
        #         if not os.path.isfile(wl_path):
        #             print('  {}[!]{} {} not found'.format(color.RED, color.END, wl_path))
        #             sys.exit(4)
        if self.artists:
            self.artists = self.artists.split(',')
