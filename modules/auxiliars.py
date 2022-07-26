#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - auxiliar functions module

import os, datetime


def clear():
    """Clear the screen. Works on Windows and Linux."""
    os.system(['clear', 'cls'][os.name == 'nt'])

def is_empty(variable):
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

def append_wordlist_to_file(filepath, wordlist):
    """
    Save wordlist into filepath provided (creates it if not exists, add words to the end if exists).
    :param filepath: path to file
    :param wordlist: list of words to save
    :return: True or False
    """
    try:
        with open(filepath, 'a') as f:
            for word in wordlist:
                f.write(word + '\n')
        return True
    except:
        return False


def remove_duplicates_from_file(infile_path, outfile_path="temp.000000000.bopscrk"):
    lines_seen = set()  # holds lines already seen
    outfile = open(outfile_path, "w")
    infile = open(infile_path, "r")
    for line in infile:
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    infile.close()
    os.remove(infile_path)
    os.rename(outfile_path, infile_path)