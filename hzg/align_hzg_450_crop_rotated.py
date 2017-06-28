#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example to align the HZG nano tomography projections.
"""

from __future__ import print_function
import tomopy
import dxchange
import alignment
import numpy as np

if __name__ == '__main__':
    # Set path to the micro-CT data to align.
    fname = '/local/decarlo/data/hzg/nanotomography/scan_renamed_450projections_crop_rotate'
    fname1 = fname + '/radios_rotated/image_00000.tiff'
    
    # for scan_renamed_450projections
    proj_start = 0
    proj_end = 451
    
    # Set binning and number of iterations
    binning = 0
    iters = 40

    ind_tomo = range(proj_start, proj_end)

    print(fname1)
    # Read normalized, centered and -log() data generated by the Doga's alignment routine.
    data = dxchange.read_tiff_stack(fname1, ind=ind_tomo, digit=5)

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(data.shape[0])

    print(data.shape)
    data = tomopy.downsample(data, level=binning, axis=1)
    data = tomopy.downsample(data, level=binning, axis=2)
    print(data.shape)
    
    fdir = fname + '_aligned' + '/align_iter_' + str(iters)
    print(fdir)
    cprj, sx, sy, conv = alignment.align_seq(data, theta, fdir=fdir, iters=iters, pad=(10, 10), blur=True, save=True, debug=True)

    np.save(fdir + '/shift_x', sx)
    np.save(fdir + '/shift_y', sy)

    # Write aligned projections as stack of TIFs.
    dxchange.write_tiff_stack(cprj, fname=fdir + '/radios/image')
