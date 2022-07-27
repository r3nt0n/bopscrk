#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk


from setuptools import setup, find_packages

# Read project description
with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name='bopscrk',
    author='r3nt0n',
    author_email='r3nt0n@protonmail.com',
    url='https://github.com/r3nt0n/bopscrk',
    version='2.4.2',
    license='GNU General Public License v3.0',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    #packages=['modules',],
    packages=find_packages(),
    scripts=['bopscrk.py'],
    install_requires=['requests'],
    entry_points = {
        'console_scripts':[
            'bopscrk = modules.main:run'
        ]
    }
)
