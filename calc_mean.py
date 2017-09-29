def calc_mean(v,emax=2.0,nrpt=10,nmin=1):
    indx = np.where(np.isfinite(v))[0]
    for n in range(nrpt):
        vc = v[indx]
        vm = vc.mean()
        ve = vc.std()
        cnd = (np.fabs(vc-vm) < ve*emax)
        indx = indx[cnd]
        if (indx.size == vc.size) or (indx.size < nmin):
            break
    return vm,ve,vc.size
