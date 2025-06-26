#!/usr/bin/env python
import os
import sys
import re

if(len(sys.argv) != 2):
    raise ValueError(f'Usage: {os.path.basename(sys.argv[0])} input_file_name')
elif(not os.path.exists(sys.argv[1])):
    raise IOError(f'Error, no such file >>> {sys.argv[1]}')

with open(sys.argv[1]) as fp:
    lines = fp.readlines()

for i,line in enumerate(lines):
    m = re.search('^(\s+)\S+',line)
    if(not m):
        continue
    index = m.group(1)
    print(f'{i+1:8d} {len(index)}')
