#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - auxiliar functions module

import os, datetime


def clear():
    """Clear the screen. Works on Windows and Linux."""
    os.system(['clear', 'cls'][os.name == 'nt'])


def remove_by_lengths(wordlist, minLength, maxLength):
    '''
    expect a list, return a new list with the values between min and max length provided
    '''
    new_wordlist = []
    for word in wordlist:
        #if (len(str(word)) < minLength) or (len(str(word)) > maxLength): wordlist.remove(word)
        if (len(str(word)) >= minLength) and (len(str(word)) <= maxLength): new_wordlist.append(str(word))
    return new_wordlist


def exclude(word, words_to_exclude):
    if word == 'john1234' and words_to_exclude == 'john1234': pass
    if word not in words_to_exclude:
        return word


def isEmpty(variable):
    """
    Check if a variable (in a type convertible to string) is empty. Returns True or False
    """
    empty = False
    if len(str(variable)) == 0:
        empty = True
    return empty


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