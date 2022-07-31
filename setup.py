#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk

# packages with python3 setup.py -v sdist

from setuptools import setup, find_packages

# Read project description
with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name='bopscrk',
    author='r3nt0n',
    author_email='r3nt0n@protonmail.com',
    url='https://github.com/r3nt0n/bopscrk',
    version='2.4.4',
    license='GNU General Public License v3.0',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
        # If any package contains *.ini files, include them
        '': ['*.cfg'],
    },
    #packages=['modules',],
    #packages=find_packages(),
    packages=['bopscrk', 'bopscrk.modules', 'bopscrk.modules.lyricpass'],
    #scripts=['bopscrk/bopscrk.py'],
    install_requires=['requests'],
    entry_points = {
        'console_scripts':[
            #'bopscrk = bopscrk.modules.main:run'
            'bopscrk = bopscrk.bopscrk:start'
        ]
    }
)
