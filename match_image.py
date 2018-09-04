#!/usr/bin/env python
import os
import sys
import numpy as np
import cv2
from scipy.ndimage import shift,zoom
from scipy.interpolate import splrep,splev
import matplotlib.pylab as plt
import matplotlib.cm as cm
from optparse import OptionParser,IndentedHelpFormatter

# Default values
ROTATE_MIN = -5.0 # deg
ROTATE_MAX = 5.0 # deg
ROTATE_STP = 0.1 # deg
SCALE_MIN = 0.9
SCALE_MAX = 1.1
SCALE_STP = 0.01
TEMPLATE_WIDTH = 100 # pixel
TEMPLATE_HEIGHT = 100 # pixel

# Read options
parser = OptionParser(formatter=IndentedHelpFormatter(max_help_position=200,width=200))
parser.add_option('-r','--rotate_min',default=ROTATE_MIN,type='float',help='Min rotation angle in deg (%default)')
parser.add_option('-R','--rotate_max',default=ROTATE_MAX,type='float',help='Max rotation angle in deg (%default)')
parser.add_option('--rotate_stp',default=ROTATE_STP,type='float',help='Step rotation angle in deg (%default)')
parser.add_option('-m','--scale_min',default=SCALE_MIN,type='float',help='Min scale_factor (%default)')
parser.add_option('-M','--scale_max',default=SCALE_MAX,type='float',help='Max scale_factor (%default)')
parser.add_option('--scale_stp',default=SCALE_STP,type='float',help='Step scale factor (%default)')
parser.add_option('--template_width',default=TEMPLATE_WIDTH,type='int',help='Template width in pixel (%default)')
parser.add_option('--template_height',default=TEMPLATE_HEIGHT,type='int',help='Template height in pixel (%default)')
parser.add_option('--template_x',default=None,type='int',help='Template X center in pixel (%default)')
parser.add_option('--template_y',default=None,type='int',help='Template Y center in pixel (%default)')
(opts,args) = parser.parse_args()

if len(args) != 2:
    sys.stderr.write('Usage: match_image.py source_image target_image\n')
    sys.exit()

src_img = cv2.imread(args[0],cv2.IMREAD_GRAYSCALE)
tgt_img = cv2.imread(args[1],cv2.IMREAD_GRAYSCALE)
if opts.template_x is None:
    opts.template_x = src_img.shape[1]//2
    opts.template_y = src_img.shape[0]//2
src_x1 = opts.template_x-opts.template_width//2
src_x2 = src_x1+opts.template_width
src_y1 = opts.template_y-opts.template_height//2
src_y2 = src_y1+opts.template_height
template = src_img[src_y1:src_y2,src_x1:src_x2]

func_x = []
func_y = []
for scale in np.arange(opts.scale_min,opts.scale_max+0.1*opts.scale_stp,opts.scale_stp):
    tst_img = zoom(tgt_img,scale)
    result = cv2.matchTemplate(tst_img,template,cv2.TM_CCOEFF_NORMED)
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
    tst_x1 = max_loc[0]
    tst_x2 = tst_x1+opts.template_width
    tst_y1 = max_loc[1]
    tst_y2 = tst_y1+opts.template_height
    coef = np.corrcoef(src_img[src_y1:src_y2,src_x1:src_x2].flatten(),tst_img[tst_y1:tst_y2,tst_x1:tst_x2].flatten())[0,1]
    func_x.append(scale)
    func_y.append(coef)
    sys.stderr.write('{:15.10f} {:13.6e}\n'.format(scale,coef))
func_x = np.array(func_x)
func_y = np.array(func_y)
func_xi = np.linspace(func_x.min(),func_x.max(),func_x.size*100)
func_yi = splev(func_xi,splrep(func_x,func_y,s=1.0e-6))
scale_optimized = func_xi[np.argmax(func_yi)]
tst_img = zoom(tgt_img,scale_optimized)
result = cv2.matchTemplate(tst_img,template,cv2.TM_CCOEFF_NORMED)
min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
tst_x1 = max_loc[0]
tst_x2 = tst_x1+opts.template_width
tst_y1 = max_loc[1]
tst_y2 = tst_y1+opts.template_height

out_img = np.zeros_like(src_img)
cut_x1 = min(src_x1,tst_x1)
cut_y1 = min(src_y1,tst_y1)
cut_x2 = min(src_img.shape[1]-src_x1,tst_img.shape[1]-tst_x1)
cut_y2 = min(src_img.shape[0]-src_y1,tst_img.shape[0]-tst_y1)
out_img[src_y1-cut_y1:src_y1+cut_y2,src_x1-cut_x1:src_x1+cut_x2] = tst_img[tst_y1-cut_y1:tst_y1+cut_y2,tst_x1-cut_x1:tst_x1+cut_x2]

cv2.rectangle(src_img,(src_x1,src_y1),(src_x2,src_y2),255,2)
#cv2.rectangle(tgt_img,(tgt_x1,tgt_y1),(tgt_x2,tgt_y2),255,2)
