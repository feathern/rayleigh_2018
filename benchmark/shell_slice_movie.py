### NOTE:  THIS IS A PYTHON 2 SCRIPT (MAYAVI USES PYTHON 2)

#  Reads in a Rayleigh shell slice file and renders data from that file
#  in 3-D using the Mayavi volume-rendering package.  You will need to have Mayavi 2
#  installed for this example to work.   
#  http://docs.enthought.com/mayavi/mayavi/

import numpy as np
import gc
from rayleigh_diagnostics import Shell_Slices



def scale_data(indata, scale_factor = 1.5, no_mean = False):
    # Rescales indata so that:
    #   1. indata has a zero spherical mean
    #   2. indata is rescaled to have min at -1, max at +1
    #   3. indata "saturates" at absolute values > scale_factor * stdev(indata) 
    # indata should be dimensioned [theta,phi]
    ntheta = indata.shape[0]
    nphi   = indata.shape[1]
    #Subtract the spherical mean
    if (no_mean):
        indata[:,:] = indata[:,:] - np.mean(indata)
    sigma = np.std(indata)
    data_lim = scale_factor*sigma
    for i in range(ntheta):
        for j in range(nphi):
            if (indata[i,j] > data_lim):
                indata[i,j] = data_lim
            if (indata[i,j] < -data_lim):
                indata[i,j] = -data_lim
            indata[i,j] = indata[i,j]/data_lim

def gen_shell_movie(allfiles, my_rank, ncpu, foffset, qind=1, hill_size=0.005):
    from rayleigh_diagnostics import Equatorial_Slices
    import numpy
    from mayavi import mlab
    mlab.options.offscreen = True


    nfiles = len(allfiles)
    dfiles = nfiles//ncpu
    my_start = my_rank*dfiles

    fmod = nfiles%ncpu
    if (my_rank < fmod):
        my_start = my_start+my_rank
        dfiles = dfiles+1
    else:
        my_start = my_start+fmod
    my_end = my_start+dfiles



    save_rendering = True  # Set to True to save an image (you lose the 3-D interactive window)


    # Radial component of velocity gives the elevation and the color
    hillsize = hill_size # 0.005 by default
    elevation_scale_factor = 1.5


    color_scale_factor = 1.5
    data_initialized = False
    for i in range(my_start, my_end):
        if (my_rank == 0):
            print('  Processing file ', i-my_start+1, 'of',my_end-my_start)
        shellfile = allfiles[i]

        shell1 = Shell_Slices(shellfile, path='./')
        radii = shell1.radius
        nphi = shell1.nphi
        ntheta = shell1.ntheta
        niter = shell1.niter
        joffset = foffset*niter
        if (not data_initialized):
                data_initialized = True
                color_data1 = np.zeros((ntheta,nphi), dtype='float64')
                color_data2 = np.zeros((ntheta,nphi), dtype='float64')
                color_data3 = np.zeros((ntheta,nphi), dtype='float64')

                x1 = np.zeros((ntheta,nphi), dtype='float64')
                x2 = np.zeros((ntheta,nphi), dtype='float64')
                x3 = np.zeros((ntheta,nphi), dtype='float64')

                y1 = np.zeros((ntheta,nphi), dtype='float64')
                y2 = np.zeros((ntheta,nphi), dtype='float64')
                y3 = np.zeros((ntheta,nphi), dtype='float64')

                z1 = np.zeros((ntheta,nphi), dtype='float64')
                z2 = np.zeros((ntheta,nphi), dtype='float64')
                z3 = np.zeros((ntheta,nphi), dtype='float64')

                r1 = np.zeros((ntheta,nphi), dtype='float64')
                r2 = np.zeros((ntheta,nphi), dtype='float64')
                r3 = np.zeros((ntheta,nphi), dtype='float64')


                pi = np.pi
                cos = np.cos
                sin = np.sin
                phi, theta = np.mgrid[0:pi:ntheta*1j, 0:2 * pi:nphi*1j]



        for j in range(niter):
            jstring = "{:0>8d}".format(j+niter*i+joffset)
            savefile = 'shell_pngs/'+jstring+'.png'

            qi = shell1.lut[qind]
            
            
            color_data1[:,:] = np.transpose(shell1.vals[:,:,0,qi,j].reshape(nphi,ntheta)) - np.mean(shell1.vals[:,:,0,qi,j])
            color_data2[:,:] = np.transpose(shell1.vals[:,:,1,qi,j].reshape(nphi,ntheta)) - np.mean(shell1.vals[:,:,1,qi,j])
            color_data3[:,:] = np.transpose(shell1.vals[:,:,2,qi,j].reshape(nphi,ntheta)) - np.mean(shell1.vals[:,:,2,qi,j])
            
	    

            # Scale both the elevation and the color data as desired
            # If rendering something with a spherical mean, set no_mean = True 
            # in the call to scale_data (as with temperature/entropy)

            scale_data(color_data1, scale_factor = color_scale_factor)
            scale_data(color_data2, scale_factor = color_scale_factor)
            scale_data(color_data3, scale_factor = color_scale_factor)

            # Create a spherical grid
            rmean = 0.3    
            rmean2 = 0.3 
            rmean3 = 0.3 
            
            # Add elevation to our globe (perturbations about rmean)
            r1[:,:] = hillsize*color_data1+rmean

            # Recast in terms of x,y,z
            x1[:,:] = r1 * sin(phi) * cos(theta)
            y1[:,:] = r1 * sin(phi) * sin(theta)
            z1[:,:] = r1 * cos(phi)
            
            # Add elevation to our globe (perturbations about rmean)
            r2[:,:] = hillsize*color_data2+rmean2

            # Recast in terms of x,y,z
            x2[:,:] = r2 * sin(phi) * cos(theta)
            y2[:,:] = r2 * sin(phi) * sin(theta)
            z2[:,:] = r2 * cos(phi)
            
            # Add elevation to our globe (perturbations about rmean)
            r3[:,:] = hillsize*color_data3+rmean3

            # Recast in terms of x,y,z
            x3[:,:] = r3 * sin(phi) * cos(theta)
            y3[:,:] = r3 * sin(phi) * sin(theta)
            z3[:,:] = r3 * cos(phi)


            # Set up the window
            winsize = 512
            winx = winsize * 3.0
            winy = winsize
            mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(winx, winy))
            mlab.clf()

            # Render topology using elevation_data (x,y,z) and color using color_data
            mlab.mesh(x1 + rmean*2.4, y1 , z1, scalars=-color_data1, colormap='RdYlBu')
            mlab.mesh(x2 , y2 , z2, scalars=-color_data2, colormap='RdYlBu')
            mlab.mesh(x3 - rmean*2.4, y3 , z3, scalars=-color_data3, colormap='RdYlBu')


            # Set the scene parameters and render

            azimuth_angle = 90
            elevation_angle = 70
            view_distance = 2.0  # was 1.3
            mlab.view(azimuth = azimuth_angle, elevation = elevation_angle, distance = view_distance)
            if (save_rendering):
                mlab.savefig(savefile) 
            else:
                mlab.show() 

from rayleigh_diagnostics import build_file_list
from mpi4py import MPI
import sys
###########################
# Initialize Communication
comm_world = MPI.COMM_WORLD
my_rank = comm_world.rank
ncpu = comm_world.size
this_batch = int(sys.argv[1])
nbatch = int(sys.argv[2])

if (len(sys.argv) > 3):
   qindex = int(sys.argv[3])
else:
   qindex = 1

if (len(sys.argv) > 4):
   hsize = float(sys.argv[4])
else:
   hsize = 0.005

files = build_file_list(0,1000000,path='Shell_Slices')
nfiles = len(files)

dfile = nfiles/nbatch
file_mod = nfiles % nbatch
fstart = dfile*(this_batch-1)
fend = fstart+dfile

#Add any leftovers to the last batch
if (this_batch == nbatch):
    if (file_mod != 0):
        fend = fend+file_mod

files = files[fstart:fend] 

if (my_rank == 0):
    #print(files)
    print 'This_batch: ', this_batch
    print 'NBATCH: ', nbatch
    print ' '
    print files
    print ''
    print ''

nfiles = len(files)
if (nfiles > 0):
    gen_shell_movie(files, my_rank, ncpu, fstart, qind=qindex, hill_size=hsize)

MPI.Finalize()
