#!/usr/bin/env python
import os
import numpy as np

fnams = []
times = []
for fnam in os.listdir('.'):
    fnams.append(fnam)
    times.append(os.path.getmtime(fnam))
times = np.array(times)
indxs = np.argsort(times)
fmt = '%%-%ds %%.2f'%(max([len(s) for s in fnams])+1)
j = -1
for i in range(times.size):
    indx = indxs[i]
    if i == 0:
        print fmt%(fnams[indx],0)
    else:
        print fmt%(fnams[indx],times[indx]-times[j])
    j = indx
