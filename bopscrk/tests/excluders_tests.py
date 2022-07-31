#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - excluders functions tests

import unittest

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from ..modules.excluders import compare, multithread_exclude, remove_duplicates, remove_by_lengths


class TestExcluders(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_compare(self):
        word_to_exclude = 'tested-password'
        word_in_wordlist = 'new-password'
        self.assertEqual('new-password', compare(word_to_exclude, word_in_wordlist))
        word_in_wordlist = 'tested-password'
        self.assertEqual(None, compare(word_to_exclude, word_in_wordlist))

    def test_multithread_exclude(self):
        word_to_exclude = 'tested-password'
        wordlist = ['new-password', 'N3w_p4S$w0Rd', 'tested-password', 'anotHer.n3w.Pa$$word']
        self.assertEqual(['new-password', 'N3w_p4S$w0Rd', 'anotHer.n3w.Pa$$word'],
                         multithread_exclude(word_to_exclude, wordlist))

    def test_remove_by_duplicates(self):
        wordlist = ['duplicate-password', 'unique_password', 'duplicate-password']
        self.assertEqual(['duplicate-password', 'unique_password'], remove_duplicates(wordlist))

    def test_remove_by_lengths(self):
        wordlist = ['p', 'pa', 'pas', 'pass', 'passw', 'passwo', 'passwor', 'password']
        self.assertEqual(['pass', 'passw', 'passwo'], remove_by_lengths(wordlist, 4, 6))


if __name__ == '__main__':
    unittest.main()