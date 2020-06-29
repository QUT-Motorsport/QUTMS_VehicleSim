from scipy.io import loadmat
from scipy.signal import find_peaks
import pandas as pd
from math import *
import numpy as np
from time import sleep

class Track:

    def __init__(self, mat_file, crv_name, x_name):
        self.track_data = loadmat(mat_file)
        self.struct = list(dict.keys(self.track_data))[3]
        self.crv_name = crv_name
        self.x_name = x_name

        # Read arrays into memory
        self.crv_np = self.track_data[str(self.struct)][self.crv_name][0][0][0]
        self.crv = self.crv_np.tolist()
        self.x = self.track_data[str(self.struct)][self.x_name][0][0][0]

        # Single values
        self.start_position = np.argmax(abs(self.crv_np))
        self.end_position = self.start_position - 1
        self.array_length = len(self.get_crv_np())

        # Format arrays with single values
        self.formatted_crv = np.append(self.crv_np[self.start_position:self.array_length], self.crv_np[:self.end_position + 1])
        self.formatted_crv = abs(self.formatted_crv)

        # Assign single values that require formatted arrays
        crv_array_offset = np.append(self.formatted_crv[self.start_position:self.array_length], self.formatted_crv[0:self.end_position + 1])
        self.offset = np.argmax(abs(crv_array_offset)) - self.start_position

    def get_crv(self):
        return self.crv

    def get_crv_np(self):
        return self.crv_np

    def get_x(self):
        return self.x

    def get_start_position(self):
        return self.start_position

    def get_end_position(self):
        return self.end_position

    def get_array_length(self):
        return self.array_length

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