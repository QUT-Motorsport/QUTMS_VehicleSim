from scipy.io import loadmat
from scipy.signal import find_peaks
import pandas as pd
from math import *
import numpy
from time import sleep

class Track:

    def __init__(self, mat_file, crv_name, x_name):
        self.track_data = loadmat(mat_file)
        self.struct = list(dict.keys(self.track_data))[3]
        self.crv_name = crv_name
        self.x_name = x_name

        # Read arrays into memory
        self.crv_np = self.track_data[str(self.struct)][self.crv_name][0][0][0]
        self.x = self.track_data[str(self.struct)][self.x_name][0][0][0]

        # Single values and crv
        self.crv = []
        self.max_abs_value = max(abs(x) for x in self.crv_np)
        for num, data in enumerate(self.crv_np):
            self.crv.append(data)  
            if abs(data) == self.get_max_abs_value():
                self.start_position = num

        # Format arrays with single values
        self.formatted_crv = numpy.append(self.get_crv_np()[self.get_start_position():self.get_array_length()], self.get_crv_np()[:self.get_end_position() + 1])
        self.formatted_crv = abs(self.formatted_crv)

        # Assign single values that require formatted arrays
        crv_array_offset = numpy.append(self.get_formatted_crv()[self.get_start_position():self.get_array_length()], self.get_formatted_crv()[0:self.get_end_position() + 1])
        abs_ofsts = [abs(x) for x in crv_array_offset]
        offset_position = abs_ofsts.index(max(abs_ofsts))
        self.offset = offset_position - self.get_start_position()

    def get_crv(self):
        return self.crv

    def get_crv_np(self):
        return self.crv_np

    def get_x(self):
        return self.x

    def get_max_abs_value(self):
        return self.max_abs_value

    def get_start_position(self):
        return self.start_position

    def get_end_position(self):
        return self.get_start_position() - 1

    def get_array_length(self):
        return len(self.get_crv_np())

    def get_formatted_crv(self):
        return self.formatted_crv

    def get_offset(self):
        return self.offset

    def get_track(self):
        track = {}
        track["offset"] = self.get_offset()
        track["crv_array"] = self.get_formatted_crv()
        track["array_length"] = self.get_array_length()
        track["x_array"] = self.get_x()
        track["start_position"] = self.get_start_position()
        track["end_position"] = self.get_end_position()
        track["crv"] = self.get_crv()
        return track