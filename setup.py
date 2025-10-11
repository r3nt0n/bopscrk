#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk

# packages with python3 setup.py -v sdist

from setuptools import setup, find_packages

# Read version and description from the bopscrk module
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "bopscrk"))
from bopscrk import __version__, desc

# Read project description
with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name="bopfast",
    version=__version__,
    license="GNU General Public License v3.0",
    description=desc,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
        # If any package contains *.cfg files, include them
        "": ["*.cfg"],
    },
    # packages=['modules',],
    # packages=find_packages(),
    packages=["bopscrk", "bopscrk.modules"],
    install_requires=["requests", "alive-progress"],
    entry_points={"console_scripts": ["bopfast = bopscrk.bopscrk:start"]},
)
