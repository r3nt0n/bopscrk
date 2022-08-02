#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk

# packages with python3 setup.py -v sdist

from setuptools import setup, find_packages
from bopscrk.bopscrk import __version__, desc

# Read project description
with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name='bopscrk',
    version=__version__,
    url='https://github.com/r3nt0n/bopscrk',
    author='r3nt0n',
    author_email='r3nt0n@protonmail.com',
    license='GNU General Public License v3.0',
    description=desc,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
        # If any package contains *.cfg files, include them
        '': ['*.cfg'],
    },
    #packages=['modules',],
    #packages=find_packages(),
    packages=['bopscrk', 'bopscrk.modules', 'bopscrk.modules.lyricpass'],
    #scripts=['bopscrk/bopscrk.py'],
    install_requires=['requests', 'alive-progress'],
    entry_points = {
        'console_scripts':[
            #'bopscrk = bopscrk.modules.main:run'
            'bopscrk = bopscrk.bopscrk:start'
        ]
    }
)
