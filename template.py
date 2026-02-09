import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#x,y = np.loadtxt('',usecols=(0,1),unpack=True)
x,y = np.loadtxt('',unpack=True)

plt.interactive(True)
if plt.fignum_exists(1):
    fig = plt.figure(1)
else;
    fig = plt.figure(1,facecolor='w',figsize=(6,3.5))
plt.subplots_adjust(top=0.85,bottom=0.20,left=0.15,right=0.90)
fig.clear()
ax1 = plt.subplot(111)
ax1.minorticks_on()
#ax1.grid(True)
#ax1.set_xscale('log')
#ax1.set_yscale('log')
ax1.plot(x,y,'b-',label='')
#ax1.set_xlim(0.0,1.0)
#ax1.set_ylim(0.0,1.0)
ax1.set_xlabel('')
ax1.set_ylabel('')
#ax1.xaxis.set_major_locator(plt.MultipleLocator(0.5))
#ax1.yaxis.set_major_locator(plt.MultipleLocator(0.5))
#ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
#ax1.yaxis.set_major_locator(plt.MaxNLocator(5))
ax1.xaxis.set_tick_params(pad=7)
ax1.yaxis.set_label_coords(-0.10,0.5)
#ax1.legend(prop={'size':12},numpoints=1)
#plt.savefig('')
plt.draw()
