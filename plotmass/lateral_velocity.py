from scipy.signal import find_peaks
import pandas as pd
import numpy
from math import sqrt

class LateralVelocity:

    def __init__(self, vehicle, track):
        self.vehicle = vehicle
        self.array_length = track.get_array_length()
        self.crv_array = track.get_formatted_crv()

    def nthroot(self, num, root):
        answer = num ** (1/root)
        return answer

    def get_lat_velocity(self):
        # For ease of access
        P = self.vehicle.get_power()
        p = self.vehicle.get_air_density()
        Cd = self.vehicle.get_coefficient_of_drag()
        A = self.vehicle.get_reference_area()
        Cl = self.vehicle.get_coefficient_of_lift()
        m = self.vehicle.get_mass()
        g = self.vehicle.get_gravity()
        mu = self.vehicle.get_coefficient_of_friction()

        radius = []
        for entry in self.crv_array:
            radius.append(1/entry)       
        top_speed = self.nthroot((2*P)/(p*Cd*A),3)
        lat_velocity = []
        for n in radius:
            weighted_load = 0.5*n*p*-Cl*A*mu
            if weighted_load > m:
                vel = top_speed
            else:
                vel = sqrt((n * mu * m * g) / (m - weighted_load))
                if vel > top_speed:
                    vel = top_speed
            lat_velocity.append(vel)
        return lat_velocity

    def get_inv_lat_velocity(self):
        inv_lat_velocity = []
        for x in self.get_lat_velocity():
            inv_lat_velocity.append(1/x)
        return inv_lat_velocity

    def get_peak_loc(self):
        return find_peaks(self.get_inv_lat_velocity())[0]

