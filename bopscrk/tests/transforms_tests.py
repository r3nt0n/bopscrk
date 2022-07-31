#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - transform functions tests

import unittest

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from ..modules.transforms import case_transforms, leet_transforms, multithread_transforms, \
                           take_initials, artist_space_transforms, lyric_space_transforms


class TestTransforms(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_leet_transform(self):
        word = 'aeiost'
        self.assertEqual(63, len(leet_transforms(word)))

    def test_case_transform(self):
        word = 'hello'
        self.assertEqual(9, len(case_transforms(word)))

    def test_multithread_transform(self):
        wordlist = ['hello', 'world', 'lorem', 'ipsum']
        self.assertEqual(33, len(multithread_transforms(case_transforms, wordlist)))
        self.assertEqual(10, len(multithread_transforms(leet_transforms, wordlist)))

    def test_take_initials(self):
        word = 'hello world lorem ipsum'
        self.assertEqual('hwli', take_initials(word))

    def test_lyric_space_transform(self):
        word = 'hello world lorem ipsum'
        self.assertEqual(11, len(lyric_space_transforms(word)))

    def test_artist_lyric_space_transform(self):
        word = 'hello world lorem ipsum'
        self.assertEqual(11, len(artist_space_transforms(word)))


if __name__ == '__main__':
    unittest.main()