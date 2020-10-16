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