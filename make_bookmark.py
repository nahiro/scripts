#!/usr/bin/env python
import os
import sys
import re
from datetime import datetime
from subprocess import check_output,call

datdir = '.'
start = 1
for f in sorted(os.listdir(datdir)):
    m = re.search('manago_('+'\d'*8+')\D',f)
    if not m:
        continue
    dstr = m.group(1)
    dtim = datetime.strptime(dstr,'%Y%m%d')
    fnam = os.path.join(datdir,f)
    command = 'pdfinfo'
    command += ' '+fnam
    out = check_output(command,shell=True).decode()
    npage = None
    for line in out.splitlines():
        #'Pages:          9',
        m = re.search('Pages\s*:\s*(\d+)',line)
        if m:
            npage = int(m.group(1))
    if npage is None:
        raise ValueError('Error in finding Pages >>> '+fnam)
    command = 'pdf2txt'
    command += ' -p 1'
    command += ' '+fnam
    out = check_output(command,shell=True).decode()
    nmin = -100
    subject = []
    for line in out.splitlines():
        m = re.search('^\s*(\d+)\.\s\s*(\S.*)$',line)
        if not m:
            continue
        n = int(m.group(1))
        if n <= nmin:
            break
        subject.append(m.group(2).strip())
        nmin = n
        #print(line)
    title = '/'.join(subject)
    sys.stdout.write('BookmarkBegin\n')
    sys.stdout.write('BookmarkTitle: {:%Y/%m/%d} ({})\n'.format(dtim,title))
    sys.stdout.write('BookmarkLevel: 1\n')
    sys.stdout.write('BookmarkPageNumber: {}\n'.format(start))
    sys.stdout.write('\n')
    #print(dstr,f,npage,title)
    start += npage
