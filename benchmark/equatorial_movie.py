def gen_eq_movie(allfiles, my_rank, ncpu, quantity_code=1, dpi = 300 , xypix = 512, minval=-150,maxval=150,
                 title_text='', cbar_text='', remove_mean=True):

    from rayleigh_diagnostics import Equatorial_Slices
    import numpy
    import matplotlib.pyplot as plt
    from matplotlib import ticker, font_manager    

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




    #Before making the plots, set up the grid
    es = Equatorial_Slices(allfiles[0],path='')


    nr = es.nr
    nphi = es.nphi
    r = es.radius/numpy.max(es.radius)
    phi = numpy.zeros(nphi+1,dtype='float64')
    phi[0:nphi] = es.phi
    phi[nphi] = numpy.pi*2  # For display purposes, it is best to have a redunant data point at 0,2pi

    #We need to generate a cartesian grid of x-y coordinates (both X & Y are 2-D)
    radius_matrix, phi_matrix = numpy.meshgrid(r,phi)
    X = radius_matrix * numpy.cos(phi_matrix)
    Y = radius_matrix * numpy.sin(phi_matrix)

    qind = es.lut[quantity_code] 
    field = numpy.zeros((nphi+1,nr),dtype='float64')


    colormap='jet'
    colormap='RdYlBu_r'



    for i in range(my_start,my_end):
        if (my_rank == 0):
            print('  Processing file ', i-my_start+1, 'of',my_end-my_start)
        f = allfiles[i]
        es = Equatorial_Slices(f, path='')
        niter = es.niter

        for j in range(niter):
            jstring = "{:0>8d}".format(es.iters[j])
            savefile = 'eq_pngs/'+jstring+'.png'


            field[0:nphi,:] =es.vals[:,:,qind,j]
            field[nphi,:] = field[0,:]  #replicate phi=0 values at phi=2pi


            #remove the m=0 mean if desired (usually a good idea, but not always)
            if (remove_mean):
                for i in range(nr):
                    the_mean = numpy.mean(field[:,i])
                    field[:,i] = field[:,i]-the_mean

            #Plot

            xyin=xypix/dpi
            fig, ax = plt.subplots(figsize=(xyin,xyin), dpi=dpi)
            tsize = 10     # title font size
            cbfsize = 6   # colorbar font size

            img = ax.pcolormesh(X,Y,field,cmap=colormap, vmin = minval, vmax=maxval)

            ax.axis('equal')  # Ensure that x & y axis ranges have a 1:1 aspect ratio
            ax.axis('off')    # Do not plot x & y axes

            # Plot bounding circles
            ax.plot(r[nr-1]*numpy.cos(phi), r[nr-1]*numpy.sin(phi), color='black')  # Inner circle
            ax.plot(r[0]*numpy.cos(phi), r[0]*numpy.sin(phi), color='black')  # Outer circle


            ax.set_title(title_text, fontsize=tsize)
            #colorbar ...
            cbar = plt.colorbar(img,orientation='horizontal', shrink=0.5, aspect = 10, ax=ax)
            cbar.set_label(cbar_text)

            tick_locator = ticker.MaxNLocator(nbins=5)
            cbar.locator = tick_locator
            cbar.update_ticks()
            cbar.ax.tick_params(labelsize=cbfsize)   #font size for the ticks

            t = cbar.ax.xaxis.label
            t.set_fontsize(cbfsize)  # font size for the axis title

            plt.savefig(savefile)
            plt.close()

def main():
    from rayleigh_diagnostics import build_file_list
    from mpi4py import MPI
    import sys

    ###########################
    # Initialize Communication
    comm_world = MPI.COMM_WORLD
    my_rank = comm_world.rank
    ncpu = comm_world.size


    the_qindex = int(sys.argv[1])
    the_dpi = int(sys.argv[2])
    the_xypix = int(sys.argv[3])
    ttext=sys.argv[4]
    minval=float(sys.argv[5])
    maxval=float(sys.argv[6])
    ctext=sys.argv[7]

    if (my_rank == 0):
        print('')
        print('  Generating equatorial-slice movie frames.')
        print('')
        print('  ///// Parameters //////')
        print('  DPI: ', the_dpi)
        print('  XY-PIXELS: ', the_xypix)
        print('  QUANTITY CODE: ', the_qindex)
        print(' ')

    files = build_file_list(0,1000000,path='Equatorial_Slices')

    gen_eq_movie(files, my_rank, ncpu, quantity_code=the_qindex, dpi = the_dpi, xypix = the_xypix, minval=minval, maxval=maxval,
                 title_text=ttext, cbar_text = ctext)

if (__name__ == '__main__'):
    main()
