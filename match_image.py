#!/usr/bin/env python
import os
import sys
import numpy as np
import cv2
from scipy.ndimage import shift,zoom,rotate
from scipy.interpolate import splrep,splev
import matplotlib.pylab as plt
import matplotlib.cm as cm
from optparse import OptionParser,IndentedHelpFormatter

# Default values
ANGLE_MIN = -5.0 # deg
ANGLE_MAX = 5.0 # deg
ANGLE_STP = 0.5 # deg
SCALE_MIN = 0.9
SCALE_MAX = 1.1
SCALE_STP = 0.01
TEMPLATE_WIDTH = 100 # pixel
TEMPLATE_HEIGHT = 100 # pixel
OUTPUT = 'output.png'

# Read options
parser = OptionParser(formatter=IndentedHelpFormatter(max_help_position=200,width=200))
parser.add_option('--src_channel',default=None,type='int',help='Source color channel (%default)')
parser.add_option('--tgt_channel',default=None,type='int',help='Target color channel (%default)')
parser.add_option('-r','--angle_min',default=ANGLE_MIN,type='float',help='Min rotation angle in deg (%default)')
parser.add_option('-R','--angle_max',default=ANGLE_MAX,type='float',help='Max rotation angle in deg (%default)')
parser.add_option('--angle_stp',default=ANGLE_STP,type='float',help='Step rotation angle in deg (%default)')
parser.add_option('-s','--scale_min',default=SCALE_MIN,type='float',help='Min scale_factor (%default)')
parser.add_option('-S','--scale_max',default=SCALE_MAX,type='float',help='Max scale_factor (%default)')
parser.add_option('--scale_stp',default=SCALE_STP,type='float',help='Step scale factor (%default)')
parser.add_option('-W','--template_width',default=TEMPLATE_WIDTH,type='int',help='Template width in pixel (%default)')
parser.add_option('-H','--template_height',default=TEMPLATE_HEIGHT,type='int',help='Template height in pixel (%default)')
parser.add_option('-x','--template_x',default=None,type='int',help='Template X center in pixel (%default)')
parser.add_option('-y','--template_y',default=None,type='int',help='Template Y center in pixel (%default)')
parser.add_option('-o','--output',default=OUTPUT,help='Output image name (%default)')
(opts,args) = parser.parse_args()

if len(args) != 2:
    sys.stderr.write('Usage: match_image.py source_image target_image\n')
    sys.exit()

if opts.src_channel is not None:
    src_img = cv2.imread(args[0])[:,:,opts.src_channel]
else:
    src_img = cv2.imread(args[0],cv2.IMREAD_GRAYSCALE)
if opts.tgt_channel is not None:
    tgt_img = cv2.imread(args[1])[:,:,opts.tgt_channel]
else:
    tgt_img = cv2.imread(args[1],cv2.IMREAD_GRAYSCALE)
if opts.template_x is None:
    opts.template_x = src_img.shape[1]//2
    opts.template_y = src_img.shape[0]//2
src_x1 = opts.template_x-opts.template_width//2
src_x2 = src_x1+opts.template_width
src_y1 = opts.template_y-opts.template_height//2
src_y2 = src_y1+opts.template_height
template = src_img[src_y1:src_y2,src_x1:src_x2]

angles = np.arange(opts.angle_min,opts.angle_max+0.1*opts.angle_stp,opts.angle_stp)
scales = np.arange(opts.scale_min,opts.scale_max+0.1*opts.scale_stp,opts.scale_stp)
coeffs = []
cmax = -1.0e-20
for scale in scales:
    tmp_img = zoom(tgt_img,scale)
    for angle in angles:
        tst_img = rotate(tmp_img,angle)
        result = cv2.matchTemplate(tst_img,template,cv2.TM_CCOEFF_NORMED)
        min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
        tst_x1 = max_loc[0]
        tst_x2 = tst_x1+opts.template_width
        tst_y1 = max_loc[1]
        tst_y2 = tst_y1+opts.template_height
        coeff = np.corrcoef(src_img[src_y1:src_y2,src_x1:src_x2].flatten(),tst_img[tst_y1:tst_y2,tst_x1:tst_x2].flatten())[0,1]
        coeffs.append(coeff)
        if coeff > cmax:
            sys.stderr.write('{:15.10f} {:15.10f} {:13.6e}\n'.format(angle,scale,coeff))
            cmax = coeff
coeffs = np.array(coeffs).reshape(scales.size,angles.size)
indx = np.unravel_index(np.argmax(coeffs),coeffs.shape)
tst_img = rotate(zoom(tgt_img,scales[indx[0]]),angles[indx[1]])
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
cv2.imwrite(opts.output,out_img)
