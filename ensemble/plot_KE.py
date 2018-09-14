# Plot Kinetic Energy as a function of Time

from rayleigh_diagnostics import G_Avgs, build_file_list
import matplotlib.pyplot as plt
import numpy as np

def get_data(directory):
    files = build_file_list(0, 1000000,path=directory+'/G_Avgs')
    a = G_Avgs(filename=files[0],path='')

    nfiles = len(files)
    for i,f in enumerate(files):
        a = G_Avgs(filename=f,path='')
        if (i == 0):
            nq = a.nq
            niter = a.niter
            gavgs = np.zeros((niter*nfiles,nq), dtype='float64')
            iters = np.zeros((niter*nfiles), dtype='int32')
            time = np.zeros((niter*nfiles), dtype='float64')
        i0 = i*niter
        i1 = (i+1)*niter
        gavgs[i0:i1,:] = a.vals
        time[i0:i1] = a.time
        iters[i0:i1] = a.iters

    lut = a.lut
    ke  = lut[401]

    return gavgs[:,ke], time

dir1 = "ra1e5"
dir2 = "ra2e5"
dir3 = "ra3e5"
dir4 = "ra4e5"

KE1, time1 = get_data(dir1)
KE2, time2 = get_data(dir2)
KE3, time3 = get_data(dir3)
KE4, time4 = get_data(dir4)

plt.clf()
plt.plot(time1, KE1, label=dir1)
plt.plot(time2, KE2, label=dir2)
plt.plot(time3, KE3, label=dir3)
plt.plot(time4, KE4, label=dir4)

plt.legend(loc='best', shadow=True)
plt.title('Time Trace of Kinetic Energy')
plt.xlabel('Time')
plt.ylabel('Energy')
plt.yscale('log')

savefile = 'KE_trace.pdf'
print('Saving figure to: ', savefile)
plt.savefig(savefile)

