#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -o NONE -r NONE -l NONE -s sr-nat44 -t udp .\robotnat\

import sys
from robot import run_cli
run_cli(sys.argv[1:])
