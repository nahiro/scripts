#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs

sys.stdin  = codecs.getreader('utf_8')(sys.stdin)
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

for line in sys.stdin:
    print line,
    for c in line.strip():
        value = ord(c)
        print '\\%03o\\%03o'%(value/256,value%256),
    print ''
