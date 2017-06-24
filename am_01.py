#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python example of how to read am images.
"""

from __future__ import print_function
import tomopy
import dxchange
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as pl
from matplotlib.widgets import Slider
from skimage import data, io, filters
from skimage import feature
from scipy.ndimage import gaussian_filter
import skimage.segmentation as seg
import skimage
from skimage.morphology import square
import scipy
import scipy.ndimage as ndi

def particle_bed_location(image, plot=False):
    edge = np.sum(image, axis=1)
    x = np.arange(0, edge.shape[0], 1)
    y = ndi.gaussian_filter(edge/float(np.amax(edge)), 5)
    if plot:
        plt.plot(x, y)
        plt.show()
    return np.abs(y - 0.5).argmin()

def laser_on(rdata, particle_bed_ref, alpha=0.8):
    nimages = rdata.shape[0]
    status = np.empty(nimages)

    for index in range(nimages):
        ndata = rdata[index]
        edge = np.sum(ndata, axis=1)
        y = ndi.gaussian_filter(edge/float(np.amax(edge)), 5)
        particle_bed = np.abs(y - 0.5).argmin()

        if particle_bed_ref >= particle_bed :
            status[index] = False
        else:
            status[index] = True
            particle_bed_ref = particle_bed_ref * alpha
    return status

def update(val):
    frame = int(np.around(sframe.val))
    l.set_data(ndata[frame,:,:])

if __name__ == '__main__':
    # Set path to the micro-CT data to reconstruct.
    top = '/Users/decarlo/Desktop/data/am/'
    template = '102_Ti_T046mm_U18G13_04mps_p70_D100um_100ps_longpath_S10156.tif'
    index_start = 10156
    index_end = 10162

    top = '/Users/decarlo/Desktop/data/Ti_126/'
    template = '126_Ti_T1mm_U18G13_0.3mps_p90_D100um_500ns_across_S10001.tif'
    index_start = 10001
    index_end = 10401

    ind_tomo = range(index_start, index_end)

    fname = top + template

    # Read the tiff raw data.
    rdata = dxchange.read_tiff_stack(fname, ind=ind_tomo)
    particle_bed_reference = particle_bed_location(rdata[0], plot=False)
    print("Particle bed location: ", particle_bed_reference)

    cdata = rdata[:, 0:particle_bed_reference, :]
#    print(rdata[0].shape)
#    edge = np.sum(rdata[0], axis=1)
#    x = np.arange(0, edge.shape[0], 1)
#    y = edge

#    print(x.shape)
#    print(edge.shape)
#    spl = scipy.interpolate.splrep(x,y,k=3) # no smoothing, 3rd order spline
#    ddy = scipy.interpolate.splev(x,spl,der=2) # use those knots to get second derivative 

#    print("1:", ddy.shape)
#    print("2:", min(ddy))
#    print("3:", np.argmin(ddy))
#    print("4:", np.argmin(ddy[np.argmin(ddy - 0).argmin()]))
#    print("5:", ddy[np.argmin(ddy - 0).argmin()])


    # Set the [start, end] index of the blocked images, flat and dark.
 

    flat_range = [0, 40]
    data_range = [40, 385]
    dark_range = [398, 399]

    flat = cdata[flat_range[0]:flat_range[1], :, :]
    proj = cdata[data_range[0]:data_range[1], :, :]
    dark = cdata[dark_range[0]:dark_range[1], :, :]

    ndata = tomopy.normalize(proj, flat, dark)
    ndata = tomopy.normalize_bg(ndata, air=300)
    ndata_max = np.amax(ndata)
    ndata_min = np.amin(ndata)
    print(ndata_min, ndata_max)
    ndata = ndata / ndata_max

    nimages = ndata.shape[0]
    for index in range(nimages):
        a=1
        #ndata[index, :, :] = chan_vese(ndata[index, :, :])
        #ndata[index, :, :] = seg.find_boundaries(ndata[index, :, :])
        #ndata[index, :, :] = feature.canny(ndata[index, :, :])
        ####ndata[index, :, :] = filters.sobel(ndata[index, :, :])
        #ndata[index, :, :] = filters.rank.threshold(ndata[index, :, :], square(3))
        #ndata[index, :, :] = skimage.img_as_float(ndata[index, :, :])
        #ndata[index, :, :]  = gaussian_filter(ndata[index, :, :] , 1)
    ax = pl.subplot(111)
    pl.subplots_adjust(left=0.25, bottom=0.25)

    frame = 0
    l = pl.imshow(ndata[frame,:,:], cmap='gray') #shows 256x256 image, i.e. 0th frame

    axcolor = 'lightgoldenrodyellow'
    axframe = pl.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
    sframe = Slider(axframe, 'Frame', 0, ndata.shape[0]-1, valfmt='%0.0f')

    sframe.on_changed(update)

    pl.show()

