from scipy.io import loadmat
from scipy.signal import find_peaks
import pandas as pd
from math import *
import numpy
from time import sleep

def fetch_data(mat_file, crv_name):
    # get crv_filt data from track_data
    track_data = loadmat(mat_file)
    struct = list(dict.keys(track_data))[3]
    crv = track_data[str(struct)][crv_name][0][0][0]
    try:
        x_array = track_data[str(struct)]['x'][0][0][0]
    except:
        x_array = []

    crv_abs = []

    # get max_abs_value's position in crv
    max_abs_value = max(abs(x) for x in crv)
    for num, data in enumerate(crv):
        crv_abs.append(data)  
        if abs(data) == max_abs_value:
            start_position = num

    end_position = start_position - 1

    array_length = len(crv)

    crv_array = numpy.append(crv[start_position:array_length], crv[:end_position + 1])
    crv_array_offset = numpy.append(crv_array[start_position:array_length], crv_array[0 :end_position + 1])
    
    abs_ofsts = [abs(x) for x in crv_array_offset]
    offset_position = abs_ofsts.index(max(abs_ofsts))
    offset = offset_position - start_position
    crv_array = abs(crv_array)

    return offset, crv_array, array_length, x_array, start_position, end_position, crv_abs