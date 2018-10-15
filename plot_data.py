#!/usr/bin/env python
import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from optparse import OptionParser,IndentedHelpFormatter

# Default values
WINX = 8.0
WINY = 6.0
WINL = 0.12
WINR = 0.90
WINT = 0.86
WINB = 0.12
NLOC = 1

# Read options
parser = OptionParser(formatter=IndentedHelpFormatter(max_help_position=200,width=200))
parser.set_usage('Usage: %prog file(s) [options]')
parser.add_option('-x','--xmin',default=None,type='float',help='X min (%default)')
parser.add_option('-X','--xmax',default=None,type='float',help='X max (%default)')
parser.add_option('-y','--ymin',default=None,type='float',help='Y min (%default)')
parser.add_option('-Y','--ymax',default=None,type='float',help='Y max (%default)')
parser.add_option('-i','--xcol',default=0,type='int',help='X column# (%default)')
parser.add_option('-j','--ycol',default=1,type='int',help='Y column# (%default)')
parser.add_option('-k','--ecol',default=None,type='int',help='Error column# (%default)')
parser.add_option('-n','--nrow',default=None,type='int',help='#rows to skip (%default)')
parser.add_option('-u','--xfac',default=None,type='float',help='X factor (%default)')
parser.add_option('-v','--yfac',default=None,type='float',help='Y factor (%default)')
parser.add_option('-A','--xtit',default='X',help='X title (%default)')
parser.add_option('-B','--ytit',default='Y',help='Y title (%default)')
parser.add_option('-t','--title',default=None,help='Title (%default)')
parser.add_option('-T','--subtitle',default=None,help='Sub title (%default)')
parser.add_option('-F','--fignam',default=None,help='Figure name (%default)')
parser.add_option('--last_fignam',default=None,help='Last figure name (%default)')
parser.add_option('-m','--marker',default=None,help='Marker (%default)')
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

if not opts.batch:
    plt.interactive(True)
fig = plt.figure(1)
fig.set_facecolor('w')
fig.set_size_inches((opts.winx,opts.winy),forward=True)
fig.clear()
plt.subplots_adjust(left=opts.winl,right=opts.winr,top=opts.wint,bottom=opts.winb)
if opts.fignam:
    pdf = PdfPages(opts.fignam)

for fnam in args:
    if opts.ecol is not None:
        x = []
        y = []
        e = []
        with open(fnam,'r') as fp:
            for i,line in enumerate(fp):
                if opts.nrow is not None and i < opts.nrow:
                    continue
                if opts.delimiter is not None:
                    for c in opts.delimiter:
                        line = line.replace(c,' ')
                item = line.split()
                if len(item) < 3:
                    continue
                if re.search('[^\d\s\.\+\-eE,]',item[opts.xcol]):
                    continue
                if re.search('[^\d\s\.\+\-eE,]',item[opts.ycol]):
                    continue
                if re.search('[^\d\s\.\+\-eE,]',item[opts.ecol]):
                    continue
                x.append(float(item[opts.xcol]))
                y.append(float(item[opts.ycol]))
                e.append(float(item[opts.ecol]))
        x = np.array(x)
        y = np.array(y)
        e = np.array(e)
        if opts.swap:
            t = x[:]
            x = np.array(y)
            y = np.array(t)
        if opts.xfac:
            x *= opts.xfac
        if opts.yfac:
            y *= opts.yfac
        if not opts.over:
            fig.clear()
        ax1 = plt.subplot(111)
        if opts.marker:
            ax1.errorbar(x,y,e,'-',marker=opts.marker)
        else:
            ax1.errorbar(x,y,e)
    else:
        x = []
        y = []
        with open(fnam,'r') as fp:
            for i,line in enumerate(fp):
                if opts.nrow is not None and i < opts.nrow:
                    continue
                if opts.delimiter is not None:
                    for c in opts.delimiter:
                        line = line.replace(c,' ')
                item = line.split()
                if len(item) < 2:
                    continue
                if re.search('[^\d\s\.\+\-eE,]',item[opts.xcol]):
                    continue
                if re.search('[^\d\s\.\+\-eE,]',item[opts.ycol]):
                    continue
                x.append(float(item[opts.xcol]))
                y.append(float(item[opts.ycol]))
        x = np.array(x)
        y = np.array(y)
        if opts.swap:
            t = x[:]
            x = np.array(y)
            y = np.array(t)
        if opts.xfac:
            x *= opts.xfac
        if opts.yfac:
            y *= opts.yfac
        if not opts.over:
            fig.clear()
        ax1 = plt.subplot(111)
        if opts.legend:
            if opts.marker:
                ax1.plot(x,y,'-',marker=opts.marker,label=os.path.basename(fnam))
            else:
                ax1.plot(x,y,label=os.path.basename(fnam))
        else:
            if opts.marker:
                ax1.plot(x,y,'-',marker=opts.marker)
            else:
                ax1.plot(x,y)
    if opts.logx:
        ax1.set_xscale('log')
    if opts.logy:
        ax1.set_yscale('log')
    if opts.subtitle:
        ax1.set_title(opts.subtitle,y=1.01,size=14)
    else:
        ax1.set_title(os.path.basename(fnam),y=1.01,size=14)
    if opts.title:
        plt.suptitle(opts.title,y=0.96,size=18)
    if opts.xmin is not None:
        ax1.set_xlim(left=opts.xmin)
    if opts.xmax is not None:
        ax1.set_xlim(right=opts.xmax)
    if opts.ymin is not None:
        ax1.set_ylim(bottom=opts.ymin)
    if opts.ymax is not None:
        ax1.set_ylim(top=opts.ymax)
    ax1.set_xlabel(opts.xtit)
    ax1.set_ylabel(opts.ytit)
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
        if not opts.skip:
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
