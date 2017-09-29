#!/usr/bin/env python
import sys
import numpy as np
from optparse import OptionParser,IndentedHelpFormatter

# Default values
LENG = 2
PREC = 0

# Read options
parser = OptionParser(formatter=IndentedHelpFormatter(max_help_position=200,width=200))
parser.add_option('-i','--imin',default=None,type='int',help='Min row number (%default)')
parser.add_option('-I','--imax',default=None,type='int',help='Max row number (%default)')
parser.add_option('-j','--jmin',default=None,type='int',help='Min column number (%default)')
parser.add_option('-J','--jmax',default=None,type='int',help='Max column number (%default)')
parser.add_option('-l','--leng',default=LENG,type='int',help='String length (%default)')
parser.add_option('-p','--prec',default=PREC,type='int',help='Precision (%default)')
parser.add_option('-s','--swap',default=False,action='store_true',help='Swap mode (%default)')
parser.add_option('-b','--batch',default=False,action='store_true',help='Batch mode (%default)')
(opts,args) = parser.parse_args()

if len(args) < 1:
    sys.stderr.write('Usage: print_matrix.py filename(s)\n')
    sys.exit(0)

for fnam in args:
    # Read data
    i,j,v = np.loadtxt(fnam,unpack=True)
    if opts.swap:
        nrow = len(set(j))
        ncol = len(set(i))
        v = v.reshape(ncol,nrow).swapaxes(0,1)
    else:
        nrow = len(set(i))
        ncol = len(set(j))
        v = v.reshape(nrow,ncol)

    # Set range
    if opts.imin is not None:
        imin = max(opts.imin,0)
    else:
        imin = 0
    if opts.imax is not None:
        imax = min(opts.imax+1,nrow)
    else:
        imax = nrow
    if opts.jmin is not None:
        jmin = max(opts.jmin,0)
    else:
        jmin = 0
    if opts.jmax is not None:
        jmax = min(opts.jmax+1,ncol)
    else:
        jmax = ncol

    # Print data
    form = '%%%d.%df'%(opts.leng,opts.prec)
    for itmp in range(imin,imax):
        for jtmp in range(jmin,jmax):
            sys.stdout.write(form%(v[itmp][jtmp]))
            if jtmp == jmax-1:
                sys.stdout.write('\n')
            else:
                sys.stdout.write(' ')
