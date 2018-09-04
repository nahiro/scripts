#!/usr/bin/env python
import os
import sys
import numpy as np
import cv2
from PIL import Image
import matplotlib.pylab as plt
import matplotlib.cm as cm
from optparse import OptionParser,IndentedHelpFormatter

# Default values
ROTATE_MIN = -5.0 # deg
ROTATE_MAX = 5.0 # deg
ROTATE_NUM = 10
SCALE_MIN = 0.9
SCALE_MAX = 1.1
SCALE_NUM = 10
TEMPLATE_WIDTH = 100 # pixel
TEMPLATE_HEIGHT = 100 # pixel

# Read options
parser = OptionParser(formatter=IndentedHelpFormatter(max_help_position=200,width=200))
parser.add_option('-r','--rotate_min',default=ROTATE_MIN,type='float',help='Min rotation angle in deg (%default)')
parser.add_option('-R','--rotate_max',default=ROTATE_MAX,type='float',help='Max rotation angle in deg (%default)')
parser.add_option('--rotate_num',default=ROTATE_NUM,type='int',help='Number of rotation angle (%default)')
parser.add_option('-m','--scale_min',default=SCALE_MIN,type='float',help='Min scale_factor (%default)')
parser.add_option('-M','--scale_max',default=SCALE_MAX,type='float',help='Max scale_factor (%default)')
parser.add_option('--scale_num',default=SCALE_NUM,type='int',help='Number of scale factor (%default)')
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
result = cv2.matchTemplate(tgt_img,template,cv2.TM_CCOEFF_NORMED)
min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
tgt_x1 = max_loc[0]
tgt_x2 = tgt_x1+opts.template_width
tgt_y1 = max_loc[1]
tgt_y2 = tgt_y1+opts.template_height
cv2.rectangle(src_img,(src_x1,src_y1),(src_x2,src_y2),255,2)
cv2.rectangle(tgt_img,(tgt_x1,tgt_y1),(tgt_x2,tgt_y2),255,2)
coef = np.corrcoef(src_img[src_y1:src_y2,src_x1:src_x2].flatten(),tgt_img[tgt_y1:tgt_y2,tgt_x1:tgt_x2].flatten())[0,1]
