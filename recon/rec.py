#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct a single data set.
"""

from __future__ import print_function

import os
import sys
import json
import argparse
import numpy as np
import collections

import h5py
import tomopy
import dxchange

# sirtfilter:
# conda install -c http://dmpelt.gitlab.io/sirtfilter/ sirtfilter
# conda install -c astra-toolbox astra-toolbox
import sirtfilter
   
def get_dx_dims(fname, dataset):
    """
    Read array size of a specific group of Data Exchange file.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    dataset : str
        Path to the dataset inside hdf5 file where data is located.

    Returns
    -------
    ndarray
        Data set size.
    """

    grp = '/'.join(['exchange', dataset])

    with h5py.File(fname, "r") as f:
        try:
            data = f[grp]
        except KeyError:
            return None

        shape = data.shape

    return shape


def restricted_float(x):

    x = float(x)
    if x < 0.0 or x >= 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x


def read_rot_centers(fname):

    try:
        with open(fname) as json_file:
            json_string = json_file.read()
            dictionary = json.loads(json_string)

        return collections.OrderedDict(sorted(dictionary.items()))

    except Exception as error: 
        print("ERROR: the json file containing the rotation axis locations is missing")
        print("ERROR: run: python find_center.py to create one first")
        exit()


def rec_sirtfbp(data, theta, rot_center, start=0, test_sirtfbp_iter = True):

    # Use test_sirtfbp_iter = True to test which number of iterations is suitable for your dataset
    # Filters are saved in .mat files in "./¨
    if test_sirtfbp_iter:
        nCol = data.shape[2]
        output_name = './test_iter/'
        num_iter = [50,100,150]
        filter_dict = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
        for its in num_iter:
            tomopy_filter = sirtfilter.convert_to_tomopy_filter(filter_dict[its], nCol)
            rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)
            output_name_2 = output_name + 'sirt_fbp_%iiter_slice_' % its
            dxchange.write_tiff_stack(data, fname=output_name_2, start=start, dtype='float32')

    # Reconstruct object using sirt-fbp algorithm:
    num_iter = 100
    nCol = data.shape[2]
    sirtfbp_filter = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
    tomopy_filter = sirtfilter.convert_to_tomopy_filter(sirtfbp_filter, nCol)
    rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)
    
    return rec


def reconstruct(h5fname, sino, rot_center, algorithm='gridrec'):

    sample_detector_distance = 30       # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 1.17e-4     # Detector pixel size in cm (5x: 1.17e-4, 2X: 2.93e-4)
    monochromator_energy = 25.74        # Energy of incident wave in keV
    alpha = 1e-02                       # Phase retrieval coeff.
    zinger_level = 1000                 # Zinger level for projections
    zinger_level_w = 1000               # Zinger level for white

    # Read APS 32-BM raw data.
    proj, flat, dark, theta = dxchange.read_aps_32id(h5fname, sino=sino)
        
    # zinger_removal
    proj = tomopy.misc.corr.remove_outlier(proj, zinger_level, size=15, axis=0)
    flat = tomopy.misc.corr.remove_outlier(flat, zinger_level_w, size=15, axis=0)

    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

    # remove stripes
    data = tomopy.remove_stripe_fw(data,level=7,wname='sym16',sigma=1,pad=True)

    # phase retrieval
    data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=alpha,pad=True)

    print("Raw data: ", h5fname)
    print("Center: ", rot_center)

    data = tomopy.minus_log(data)

    # Reconstruct object.
    if algorithm == 'sirtfbp':
        rec = rec_sirtfbp(data, theta, rot_center)
    else:
        algorithm = 'gridrec'
        rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')
        
    print("Algorithm: ", algorithm)

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
    
    return rec
        

def rec_full(h5fname, rot_center, algorithm):
    
    data_size = get_dx_dims(h5fname, 'data')

    # Select sinogram range to reconstruct.
    sino_start = 0
    sino_end = data_size[1]

    chunks = 16         # number of sinogram chunks to reconstruct
                        # only one chunk at the time is reconstructed
                        # allowing for limited RAM machines to complete a full reconstruction

    nSino_per_chunk = (sino_end - sino_start)/chunks
    print("Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk))            

    strt = 0
    for iChunk in range(0,chunks):
        print('\n  -- chunk # %i' % (iChunk+1))
        sino_chunk_start = sino_start + nSino_per_chunk*iChunk 
        sino_chunk_end = sino_start + nSino_per_chunk*(iChunk+1)
        print('\n  --------> [%i, %i]' % (sino_chunk_start, sino_chunk_end))
                
        if sino_chunk_end > sino_end: 
            break

        sino = (int(sino_chunk_start), int(sino_chunk_end))

        # Reconstruct.
        rec = reconstruct(h5fname, sino, rot_center, algorithm)
                
        # Write data as stack of TIFs.
        fname = os.path.dirname(h5fname) + '/' + os.path.splitext(os.path.basename(h5fname))[0]+ '_full_rec/' + 'recon'
        print("Reconstructions: ", fname)
        dxchange.write_tiff_stack(rec, fname=fname, start=strt)
        strt += sino[1] - sino[0]
    

def rec_slice(h5fname, nsino, rot_center, algorithm):
    
    data_size = get_dx_dims(h5fname, 'data')
    ssino = int(data_size[1] * nsino)

    # Select sinogram range to reconstruct
    sino = None
        
    start = ssino
    end = start + 1
    sino = (start, end)

    # Reconstruct.
    # print("============> ", h5fname, sino, rot_center, algorithm)
    # print("============> ", type(h5fname), type(sino), type(rot_center), type(algorithm))
    rec = reconstruct(h5fname, sino, rot_center, algorithm)

    fname = os.path.dirname(h5fname) + '/' + 'slice_rec/' + 'recon_' + os.path.splitext(os.path.basename(h5fname))[0]
    dxchange.write_tiff_stack(rec, fname=fname)
    print("Rec: ", fname)
    print("Slice: ", start)
    
   
def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="directory containing multiple datasets or file name of a single dataset: /data/ or /data/sample.h5")
    parser.add_argument("--axis", nargs='?', type=str, default="1024.0", help="rotation axis location: 1024.0 (default 1024.0)")
    parser.add_argument("--method", nargs='?', type=str, default="gridrec", help="reconstruction algorithm: sirtfbp (default gridrec)")
    parser.add_argument("--type", nargs='?', type=str, default="slice", help="reconstruction type: full (default slice)")
    parser.add_argument("--nsino", nargs='?', type=restricted_float, default=0.5, help="location of the sinogram used by find center (0 top, 1 bottom): 0.5 (default 0.5)")

    args = parser.parse_args()

    # Set path to the micro-CT data to reconstruct.
    fname = args.fname
    algorithm = args.method
    rot_center = float(args.axis)
    nsino = float(args.nsino)

    slice = False
    if args.type == "slice":
        slice = True

    if os.path.isfile(fname):       
        if slice:             
            rec_slice(fname, nsino, rot_center, algorithm=algorithm)
        else:
            rec_full(fname, rot_center, algorithm=algorithm)

    elif os.path.isdir(fname):
        # Add a trailing slash if missing
        top = os.path.join(fname, '')
        
        # Load the the rotation axis positions.
        jfname = top + "rotation_axis.json"
        
        dictionary = read_rot_centers(jfname)
            
        for key in dictionary:
            dict2 = dictionary[key]
            for h5fname in dict2:
                rot_center = dict2[h5fname]
                fname = top + h5fname
                if slice:             
                    rec_slice(fname, nsino, rot_center, algorithm=algorithm)
                else:
                    rec_full(fname, rot_center, algorithm=algorithm)
    else:
        print("Directory or File Name does not exist: ", fname)

if __name__ == "__main__":
    main(sys.argv[1:])
