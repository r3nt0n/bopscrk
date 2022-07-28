#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk


from .args import Arguments
from .config import Config


args = Arguments()
Config = Config(args.cfg_file)
#Config.setup()