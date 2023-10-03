#!/usr/bin/env python
# encoding: utf-8

import os

# Check if the environment variables exist, otherwise use defaults
LOC = os.getenv('LOC', './buildinfo_data/')
DB_LOC = os.getenv('DB_LOC', './bi_multi_tables.db')
MAINTAINER_INST_LOC = os.getenv('MAINTAINER_INST_LOC', "https://popcon.debian.org/maint/by_inst")
MAINTAINER_TEXT_FILE = os.getenv('MAINTAINER_TEXT_FILE', 'maintainer.txt')
MAINTAINER_CSV_FILE = os.getenv('MAINTAINER_CSV_FILE', 'maintainer.csv')
REGEX = os.getenv('REGEX', "(\ )+")
INST_LOC = os.getenv('INST_LOC', 'https://popcon.debian.org/by_inst')
POPCON_CSV = os.getenv('POPCON_CSV', 'today.csv')
POPCON_TEXT = os.getenv('POPCON_TEXT', 'today.txt')
POPCON_DATA = os.getenv('POPCON_DATA', './popcon/{}/{}/{}')
POPCON = os.getenv('POPCON', 'https://popcon.debian.org')
BUILDINFO = os.getenv('BUILDINFO', 'https://buildinfos.debian.net/ftp-master.debian.org/buildinfo/{}/{}/{}/')
