# Plot Temperature as function of Radius from Shell Averages

from rayleigh_diagnostics import Shell_Avgs, build_file_list
import matplotlib.pyplot as plt
import numpy as np

def get_data(directory):
    files = build_file_list(0, 1000000,path=directory+'/Shell_Avgs')
    a = Shell_Avgs(filename=files[-1], path='')

    nr = a.nr
    nq = a.nq
    nmom = 4
    niter = a.niter
    radius = a.radius
    savg = np.zeros((nr,nmom,nq), dtype='float64')
    for i in range(niter):
        savg[:,:,:] += a.vals[:,:,:,i]
    savg = savg*(1.0/niter)

    lut = a.lut
    thermal = lut[501]

    return savg[:,0,thermal], radius

dir1 = "ra1e5"
dir2 = "ra2e5"
dir3 = "ra3e5"
dir4 = "ra4e5"

T1, radius1 = get_data(dir1)
T2, radius2 = get_data(dir2)
T3, radius3 = get_data(dir3)
T4, radius4 = get_data(dir4)

plt.clf()
plt.plot(radius1, T1, label=dir1)
plt.plot(radius2, T2, label=dir2)
plt.plot(radius3, T3, label=dir3)
plt.plot(radius4, T4, label=dir4)

plt.legend(loc='best', shadow=True)
plt.title('Spherically Averaged Temperature')
plt.xlabel('Radius')
plt.ylabel('Temperature')

savefile = 'Temperature_mean.pdf'
print('Saving figure to: ', savefile)
plt.savefig(savefile)

