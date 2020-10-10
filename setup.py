#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk


from setuptools import setup, find_packages

setup(
    name='bopscrk',
    author='r3nt0n',
    author_email='r3nt0n@protonmail.com',
    url='https://github.com/r3nt0n/bopscrk',
    version='2.2',
    license='GNU General Public License v3.0',
    packages=['lib',],
    scripts=['bopscrk.py'],
    install_requires=['requests','beautifulsoup4'],
)
