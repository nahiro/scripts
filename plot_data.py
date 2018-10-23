#!/usr/bin/env python
import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from optparse import OptionParser,IndentedHelpFormatter

# Default values
LINESTYLE = '-'
WINX = 8.0
WINY = 6.0
WINL = 0.12
WINR = 0.90
WINT = 0.86
WINB = 0.12
NLOC = 1
XCOL = 0
YCOL = 1
XTIT = 'X'
YTIT = 'Y'
LINESTYLE = '-'
LABEL = 'file_name'

# Read options
parser = OptionParser(formatter=IndentedHelpFormatter(max_help_position=200,width=200))
parser.set_usage('Usage: %prog file(s) [options]')
parser.add_option('-x','--xmin',default=None,type='float',action='append',help='X min (%default)')
parser.add_option('-X','--xmax',default=None,type='float',action='append',help='X max (%default)')
parser.add_option('-y','--ymin',default=None,type='float',action='append',help='Y min (%default)')
parser.add_option('-Y','--ymax',default=None,type='float',action='append',help='Y max (%default)')
parser.add_option('-i','--xcol',default=None,type='int',action='append',help='X column# ({})'.format(XCOL))
parser.add_option('-j','--ycol',default=None,type='int',action='append',help='Y column# ({})'.format(YCOL))
parser.add_option('-k','--ecol',default=None,type='int',action='append',help='Error column# (%default)')
parser.add_option('-n','--nrow',default=None,type='int',action='append',help='#rows to skip (%default)')
parser.add_option('-u','--xfac',default=None,type='float',action='append',help='X factor (%default)')
parser.add_option('-v','--yfac',default=None,type='float',action='append',help='Y factor (%default)')
parser.add_option('-A','--xtit',default=None,action='append',help='X title ({})'.format(XTIT))
parser.add_option('-B','--ytit',default=None,action='append',help='Y title ({})'.format(YTIT))
parser.add_option('-t','--title',default=None,action='append',help='Title (%default)')
parser.add_option('-T','--subtitle',default=None,action='append',help='Sub title (%default)')
parser.add_option('--ls',default=None,action='append',help='Line style ({})'.format(LINESTYLE))
parser.add_option('--lc',default=None,action='append',help='Line color (%default)')
parser.add_option('-m','--marker',default=None,action='append',help='Marker (%default)')
parser.add_option('--mfc',default=None,action='append',help='Marker face color (%default)')
parser.add_option('--mec',default=None,action='append',help='Marker edge color (%default)')
parser.add_option('--label',default=None,action='append',help='Label ({})'.format(LABEL))
parser.add_option('-F','--fignam',default=None,help='Figure name (%default)')
parser.add_option('--last_fignam',default=None,help='Last figure name (%default)')
parser.add_option('-d','--delimiter',default=None,action='append',help='Delimiter (%default)')
parser.add_option('--winx',default=WINX,type='float',help='Window X size in inch (%default)')
parser.add_option('--winy',default=WINY,type='float',help='Window Y size in inch (%default)')
parser.add_option('--winl',default=WINL,type='float',help='Window left (%default)')
parser.add_option('--winr',default=WINR,type='float',help='Window right (%default)')
parser.add_option('--wint',default=WINT,type='float',help='Window top (%default)')
parser.add_option('--winb',default=WINB,type='float',help='Window bottom (%default)')
parser.add_option('--nloc',default=NLOC,type='int',help='Legend location (%default)')
parser.add_option('--legend',default=False,action='store_true',help='Draw legend (%default)')
parser.add_option('-l','--logx',default=False,action='store_true',help='Logscale X (%default)')
parser.add_option('-L','--logy',default=False,action='store_true',help='Logscale Y (%default)')
parser.add_option('-s','--swap',default=False,action='store_true',help='Swap mode (%default)')
parser.add_option('-o','--over',default=False,action='store_true',help='Over plot mode (%default)')
parser.add_option('-S','--skip',default=False,action='store_true',help='Skip mode (%default)')
parser.add_option('-b','--batch',default=False,action='store_true',help='Batch mode (%default)')
(opts,args) = parser.parse_args()
if len(args) > 0:
    fnams = args
else:
    parser.print_usage()
    sys.exit()
if opts.xcol is None:
    opts.xcol = [XCOL]
if opts.ycol is None:
    opts.ycol = [YCOL]
if opts.xtit is None:
    opts.xtit = [XTIT]
if opts.ytit is None:
    opts.ytit = [YTIT]
if opts.ls is None:
    opts.ls = [LINESTYLE]
if opts.lc is not None and opts.mfc is None:
    opts.mfc = opts.lc
if opts.mfc is not None and opts.mec is None:
    opts.mec = opts.mfc
nplot = len(fnams)
gv = globals()
params = ['xmin','xmax','ymin','ymax','xcol','ycol','ecol','nrow','xfac','yfac','xtit','ytit','title','subtitle','ls','lc','marker','mfc','mec','label']
for param in params:
    p = getattr(opts,param)
    if p is not None:
        if len(p) > nplot:
            nplot = len(p)
    gv[param] = []
fs = []
for i in range(nplot):
    for param in params:
        p = getattr(opts,param)
        if p is not None:
            indx = -1 if i >= len(p) else i
            if type(p[indx]) is float and np.isnan(p[indx]):
                gv[param].append(None)
            elif type(p[indx]) is int and p[indx] < 0:
                gv[param].append(None)
            elif type(p[indx]) is str and len(p[indx]) < 1:
                gv[param].append(None)
            else:
                gv[param].append(p[indx])
        else:
            gv[param].append(None)
    if i >= len(fnams):
        fs.append(fnams[-1])
    else:
        fs.append(fnams[i])
        if label[i] is None:
            label[i] = os.path.basename(fs[i])

if not opts.batch:
    plt.interactive(True)
fig = plt.figure(1)
fig.set_facecolor('w')
fig.set_size_inches((opts.winx,opts.winy),forward=True)
fig.clear()
plt.subplots_adjust(left=opts.winl,right=opts.winr,top=opts.wint,bottom=opts.winb)
if opts.fignam:
    pdf = PdfPages(opts.fignam)

for i in range(nplot):
    fnam = fs[i]
    if ecol[i] is not None:
        x = []
        y = []
        e = []
        with open(fnam,'r') as fp:
            for n,line in enumerate(fp):
                if nrow[i] is not None and n < nrow[i]:
                    continue
                if opts.delimiter is not None:
                    for c in opts.delimiter:
                        line = line.replace(c,' ')
                item = line.split()
                if len(item) < 3:
                    continue
                if re.search('[^\d\s\.\+\-eE,]',item[xcol[i]]):
                    continue
                if re.search('[^\d\s\.\+\-eE,]',item[ycol[i]]):
                    continue
                if re.search('[^\d\s\.\+\-eE,]',item[ecol[i]]):
                    continue
                x.append(float(item[xcol[i]]))
                y.append(float(item[ycol[i]]))
                e.append(float(item[ecol[i]]))
        x = np.array(x)
        y = np.array(y)
        e = np.array(e)
        if opts.swap:
            t = x[:]
            x = np.array(y)
            y = np.array(t)
        if xfac[i]:
            x *= xfac[i]
        if yfac[i]:
            y *= yfac[i]
        if not opts.over:
            fig.clear()
            ax1 = plt.subplot(111)
        elif i == 0:
            ax1 = plt.subplot(111)
        if opts.legend:
            if marker[i]:
                ax1.errorbar(x,y,e,ls=ls[i],color=lc[i],marker=marker[i],mfc=mfc[i],mec=mec[i],label=label[i])
            else:
                ax1.errorbar(x,y,e,ls=ls[i],color=lc[i],label=label[i])
        else:
            if marker[i]:
                ax1.errorbar(x,y,e,ls=ls[i],color=lc[i],marker=marker[i],mfc=mfc[i],mec=mec[i])
            else:
                ax1.errorbar(x,y,e,ls=ls[i],color=lc[i])
    else:
        x = []
        y = []
        with open(fnam,'r') as fp:
            for n,line in enumerate(fp):
                if nrow[i] is not None and n < nrow[i]:
                    continue
                if opts.delimiter is not None:
                    for c in opts.delimiter:
                        line = line.replace(c,' ')
                item = line.split()
                if len(item) < 2:
                    continue
                if re.search('[^\d\s\.\+\-eE,]',item[xcol[i]]):
                    continue
                if re.search('[^\d\s\.\+\-eE,]',item[ycol[i]]):
                    continue
                x.append(float(item[xcol[i]]))
                y.append(float(item[ycol[i]]))
        x = np.array(x)
        y = np.array(y)
        if opts.swap:
            t = x[:]
            x = np.array(y)
            y = np.array(t)
        if xfac[i]:
            x *= xfac[i]
        if yfac[i]:
            y *= yfac[i]
        if not opts.over:
            fig.clear()
            ax1 = plt.subplot(111)
        elif i == 0:
            ax1 = plt.subplot(111)
        if opts.legend:
            if marker[i]:
                ax1.plot(x,y,ls=ls[i],color=lc[i],marker=marker[i],mfc=mfc[i],mec=mec[i],label=label[i])
            else:
                ax1.plot(x,y,ls=ls[i],color=lc[i],label=label[i])
        else:
            if marker[i]:
                ax1.plot(x,y,ls=ls[i],color=lc[i],marker=marker[i],mfc=mfc[i],mec=mec[i])
            else:
                ax1.plot(x,y,ls=ls[i],color=lc[i])
    if opts.logx:
        ax1.set_xscale('log')
    if opts.logy:
        ax1.set_yscale('log')
    if subtitle[i]:
        ax1.set_title(subtitle[i],y=1.01,size=14)
    else:
        ax1.set_title(os.path.basename(fnam),y=1.01,size=14)
    if title[i]:
        plt.suptitle(title[i],y=0.96,size=18)
    if xmin[i] is not None:
        ax1.set_xlim(left=xmin[i])
    if xmax[i] is not None:
        ax1.set_xlim(right=xmax[i])
    if ymin[i] is not None:
        ax1.set_ylim(bottom=ymin[i])
    if ymax[i] is not None:
        ax1.set_ylim(top=ymax[i])
    ax1.set_xlabel(xtit[i])
    ax1.set_ylabel(ytit[i])
    ax1.xaxis.set_tick_params(pad=7)
    ax1.yaxis.set_label_coords(-0.1,0.5)
    ax1.minorticks_on()
    ax1.grid(True)
    if opts.legend:
        ax1.legend(loc=opts.nloc,frameon=False)
    if opts.fignam:
        plt.savefig(pdf,format='pdf')
    if not opts.batch:
        plt.draw()
        plt.pause(0.1)
        if not opts.skip and i < nplot-1:
            sys.stderr.write('Type \'q\' to quit.\n')
            line = sys.stdin.readline()
            if re.search('q',line):
                if opts.fignam:
                    pdf.close()
                sys.exit(0)
if opts.fignam:
    pdf.close()
if opts.last_fignam is not None:
    plt.savefig(opts.last_fignam)
