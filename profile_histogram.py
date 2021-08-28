import numpy as np

def moving_average(x,y,n=100,m=10,threshold=[5.0,2.0],
                   xmin=None,xmax=None,xstp=None,xwid=None,xmod=None,
                   ymin=None,ymax=None,fill_value=None,spread=True,center=False):
    if xmin is None:
        xmin = np.nanmin(x)
    if xmax is None:
        xmax = np.nanmax(x)
    if xstp is None:
        if center:
            xstp = (xmax-xmin)/float(n-1)
        else:
            xstp = (xmax-xmin)/float(n)
    if xwid is None:
        xwid = xstp*m
    hwid = 0.5*np.fabs(xwid)
    if xmod is not None:
        hmod = 0.5*np.fabs(xmod)
    if center:
        xorg = xmin
    else:
        xorg = xmin+0.5*xstp
    xp = np.arange(xorg,xmax+xstp*1.0e-3,xstp)
    nx = xp.size
    navg = []
    xavg = []
    xstd = []
    yavg = []
    ystd = []
    if ymin is not None:
        cnd = y >= ymin
        x = x[cnd]
        y = y[cnd]
    if ymax is not None:
        cnd = y <= ymax
        x = x[cnd]
        y = y[cnd]
    for i in range(nx):
        xdif = x-xp[i]
        if xmod is not None:
            xdif = np.mod(xdif+hmod,xmod)-hmod
        cnd = (xdif >= -hwid) & (xdif < hwid)
        if np.any(cnd):
            xc = x[cnd]
            yc = y[cnd]
            if threshold is not None:
                for e in threshold:
                    yc_mean = yc.mean()
                    yc_std = yc.std()
                    cnd = np.fabs(yc-yc_mean) < yc_std*e
                    xc = xc[cnd]
                    yc = yc[cnd]
            navg.append(xc.size)
            xavg.append(xc.mean())
            xstd.append(xc.std())
            yavg.append(yc.mean())
            ystd.append(yc.std())
        elif fill_value is not None:
            navg.append(0)
            xavg.append(xp[i])
            xstd.append(0.0)
            yavg.append(fill_value)
            ystd.append(0.0)
        else:
            navg.append(0)
            xavg.append(xp[i])
            xstd.append(0.0)
            yavg.append(np.nan)
            ystd.append(0.0)
    navg = np.array(navg)
    xavg = np.array(xavg)
    xstd = np.array(xstd)
    yavg = np.array(yavg)
    ystd = np.array(ystd)
    if not spread:
        cnd = navg > 0
        norm = 1.0/np.sqrt(np.float64(navg[cnd]))
        xstd[cnd] *= norm
        ystd[cnd] *= norm
    return xp,navg,xavg,xstd,yavg,ystd

def profile_histogram(x,y,n=10,threshold=[5.0,2.0],
                      xmin=None,xmax=None,xstp=None,xmod=None,
                      ymin=None,ymax=None,fill_value=None,spread=True,center=False):
    if xmin is None:
        xmin = np.nanmin(x)
    if xmax is None:
        xmax = np.nanmax(x)
    if xstp is None:
        if center:
            xstp = (xmax-xmin)/float(n-1)
        else:
            xstp = (xmax-xmin)/float(n)
    hwid = 0.5*np.fabs(xstp)
    if xmod is not None:
        hmod = 0.5*np.fabs(xmod)
    if center:
        xorg = xmin
    else:
        xorg = xmin+0.5*xstp
    xp = np.arange(xorg,xmax+xstp*1.0e-3,xstp)
    nx = xp.size
    navg = []
    xavg = []
    xstd = []
    yavg = []
    ystd = []
    if ymin is not None:
        cnd = y >= ymin
        x = x[cnd]
        y = y[cnd]
    if ymax is not None:
        cnd = y <= ymax
        x = x[cnd]
        y = y[cnd]
    for i in range(nx):
        xdif = x-xp[i]
        if xmod is not None:
            xdif = np.mod(xdif+hmod,xmod)-hmod
        cnd = (xdif >= -hwid) & (xdif < hwid)
        if np.any(cnd):
            xc = x[cnd]
            yc = y[cnd]
            if threshold is not None:
                for e in threshold:
                    yc_mean = yc.mean()
                    yc_std = yc.std()
                    if yc_std > 0.0:
                        cnd = np.fabs(yc-yc_mean) < yc_std*e
                        xc = xc[cnd]
                        yc = yc[cnd]
            navg.append(xc.size)
            xavg.append(xc.mean())
            xstd.append(xc.std())
            yavg.append(yc.mean())
            ystd.append(yc.std())
        elif fill_value is not None:
            navg.append(0)
            xavg.append(xp[i])
            xstd.append(0.0)
            yavg.append(fill_value)
            ystd.append(0.0)
        else:
            navg.append(0)
            xavg.append(xp[i])
            xstd.append(0.0)
            yavg.append(np.nan)
            ystd.append(0.0)
    navg = np.array(navg)
    xavg = np.array(xavg)
    xstd = np.array(xstd)
    yavg = np.array(yavg)
    ystd = np.array(ystd)
    if not spread:
        cnd = navg > 0
        norm = 1.0/np.sqrt(np.float64(navg[cnd]))
        xstd[cnd] *= norm
        ystd[cnd] *= norm
    return xp,navg,xavg,xstd,yavg,ystd

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    x = np.arange(100.0)
    nx = x.size
    y = np.random.rand(nx)
    xp,navg,xavg,xstd,yavg,ystd = profile_histogram(x,y,xmin=0.0,xmax=100.0,n=10,center=False)
    plt.interactive(True)
    fig = plt.figure(1)
    fig.set_facecolor('w')
    fig.set_size_inches((8.0,6.0),forward=True)
    fig.clear()
    ax1 = plt.subplot(111)
    ax1.minorticks_on()
    ax1.scatter(x,y)
    ax1.errorbar(xp,yavg,yerr=ystd,marker='o',mfc='None')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.xaxis.set_tick_params(pad=7)
    ax1.yaxis.set_label_coords(-0.10,0.5)
    plt.savefig('profile_histogram.pdf')
    plt.draw()
