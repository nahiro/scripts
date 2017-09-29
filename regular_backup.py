#!/usr/bin/env python
import os
import sys
from subprocess import call
from optparse import OptionParser,IndentedHelpFormatter

# Default values
DSTDIR = '/mnt/backup'
BACKUP_LIST = '/mnt/backup/list.txt'

# Read options
parser = OptionParser(formatter=IndentedHelpFormatter(max_help_position=200,width=200))
parser.add_option('-d','--dstdir',default=DSTDIR,help='Destination directory (%default)')
parser.add_option('-l','--backup_list',default=BACKUP_LIST,help='List of directories to be backed up. (%default)')
parser.set_usage('Usage: %prog [options]')
(opts,args) = parser.parse_args()

dirs = []
if not os.path.exists(opts.backup_list):
    raise IOError('No such file >>> '+opts.backup_list)
with open(opts.backup_list) as fp:
    for line in fp:
        item = line.strip()
        if item[0] == '#':
            continue
        dirs.append(item)
for d in dirs:
    if not os.path.exists(d):
        sys.stderr.write('Warning, no such directory >>> '+d)
        continue
    command = 'rsync -a --delete --relative {} {}'.format(d,opts.dstdir)
    call(command,shell=True)
