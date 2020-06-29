from scipy.signal import find_peaks
import pandas as pd
import numpy
from math import *
from numpy import *

class Momentum:

    def __init__(self, vehicle, track, peak_loc, lat_velocity):
        self.vehicle = vehicle
        self.track = track
        self.peak_loc = peak_loc
        self.lat_velocity = lat_velocity
        self.number_of_peaks = len(peak_loc)

        self.accel_velocity = []
        self.accel_a_long = []
        self.accel_a_lat = []

        self.brake_velocity = []
        self.brake_a_long = []
        self.brake_a_lat = []

    def shift_list(self, master_list, start_position=-1, end_position=-1, offset=-1):
        if start_position == -1 and end_position == -1 and offset == -1:
            start_position = self.track.get_start_position()
            end_position = self.track.get_end_position()
            offset = self.track.get_offset()

        primary_list = master_list[start_position + offset:len(master_list)]
        secondary_list = master_list[0:end_position + offset + 1]
        master_list = primary_list + secondary_list
        return master_list

    

    def calc_accel(self):
        # For ease of access
        P = self.vehicle.get_power()
        p = self.vehicle.get_air_density()
        Cd = self.vehicle.get_coefficient_of_drag()
        A = self.vehicle.get_reference_area()
        Cl = self.vehicle.get_coefficient_of_lift()
        m = self.vehicle.get_mass()
        g = self.vehicle.get_gravity()
        mu = self.vehicle.get_coefficient_of_friction()

        # Aliases and counters
        s = self.track.get_x()
        x = -1
        is_accel = False

        for nn in range(0, self.number_of_peaks + 1):

            if nn == 0:
                start_point = 0
                end_point = self.peak_loc[0] - 1
            elif nn == self.number_of_peaks:
                start_point = self.peak_loc[nn - 1]
                end_point = len(self.lat_velocity)
            else:
                start_point = self.peak_loc[nn - 1]
                end_point = self.peak_loc[nn] - 1

            for n in range(start_point, end_point + 1):
                x += 1
                if n == 0:
                    v = self.lat_velocity[0]
                    N = m*g+(0.5*p*self.lat_velocity[0]**2*-Cl*A)
                    a_resultant = (mu*N/m)
                    a_a_long_available = 0
                    a_lat = a_resultant
                elif n == start_point and is_accel and self.accel_velocity[x - 1] < self.lat_velocity[self.peak_loc[nn - 1]]:
                    v = self.accel_velocity[x - 1]
                    a_a_long_available = self.accel_a_long[x - 1]
                    a_lat = self.accel_a_lat[x - 1]
                elif n == start_point:
                    v = self.lat_velocity[start_point]
                    N = m*g+(0.5*p*self.lat_velocity[n]**2*-Cl*A)
                    a_resultant = (mu*N)/m
                    a_a_long_available = 0
                    a_lat = a_resultant
                else:
                    try:
                        distance = s[n] - s[n - 1]
                        N = m*g+(0.5*p*self.accel_velocity[x - 1]**2*-Cl*A)              
                        a_lat = self.accel_velocity[x - 1]**2*self.track.get_formatted_crv()[n]
                    except:
                        break
                    a_resultant = (mu*N)/m
                    if a_lat > a_resultant:
                        a_lat = a_resultant
                    GL_a_long_available = sqrt(a_resultant**2-a_lat**2)
                    try:
                        PL_a_long_available = ((P/self.accel_velocity[x-1])-(0.5*p*(self.accel_velocity[x-1])**2*Cd*A))/m
                    except ZeroDivisionError:
                        PL_a_long_available = 0
                    a_a_long_available = minimum(GL_a_long_available, PL_a_long_available)
                    v = sqrt((self.accel_velocity[x-1])**2+2*a_a_long_available*distance)

                if is_accel == False:
                    is_accel = True
                
                self.accel_velocity.append(v)
                self.accel_a_long.append(a_a_long_available)
                self.accel_a_lat.append(a_lat)
        
        self.accel_velocity = self.shift_list(self.accel_velocity)
        self.accel_a_long = self.shift_list(self.accel_a_long)
        self.accel_a_lat = self.shift_list(self.accel_a_lat)

    def calc_deaccel(self):
        # For ease of access
        P = self.vehicle.get_power()
        p = self.vehicle.get_air_density()
        Cd = self.vehicle.get_coefficient_of_drag()
        A = self.vehicle.get_reference_area()
        Cl = self.vehicle.get_coefficient_of_lift()
        m = self.vehicle.get_mass()
        g = self.vehicle.get_gravity()
        mu = self.vehicle.get_coefficient_of_friction()

        # Alises and counters
        array_length = self.track.get_array_length()
        x = array_length
        y = 0
        s = self.track.get_x()

        # Calculations

        for i in range(array_length):
            self.brake_velocity.append(0)
            self.brake_a_long.append(0)
            self.brake_a_lat.append(0)

        for nn in range(self.number_of_peaks, -1, -1):
            if nn == self.number_of_peaks:
                start_point = array_length - 1
                end_point = self.peak_loc[self.number_of_peaks - 1] + 1
            elif nn == 0:
                start_point = self.peak_loc[0]
                end_point = 0
            else:
                start_point = self.peak_loc[nn]
                end_point = self.peak_loc[nn - 1] + 1

            for n in range(start_point, end_point - 1, -1):
                x -= 1
                if n == self.peak_loc[0]:
                    v = self.lat_velocity[self.peak_loc[0]]
                    b_a_long_available = 0
                    N = m*g+(0.5*p*self.lat_velocity[n]**2*-Cl*A)
                    a_resultant = (mu*N)/m
                    a_lat = a_resultant
                elif n == start_point:
                    v = self.lat_velocity[start_point]
                    b_a_long_available = 0
                    N = m*g+(0.5*p*self.lat_velocity[n]**2*-Cl*A)
                    a_resultant = (mu*N)/m
                    a_lat = a_resultant
                else:
                    distance = s[n+1]-s[n]
                    N = m*g+(0.5*p*self.brake_velocity[x+1]**2*-Cl*A)
                    a_lat = self.brake_velocity[x+1]**2*self.track.get_formatted_crv()[n]
                    a_resultant = (mu*N)/m
                    if a_lat>a_resultant:
                        a_lat = a_resultant
                    b_a_long_available = sqrt(a_resultant**2-a_lat**2)
                    v = sqrt((self.brake_velocity[x+1])**2+2*b_a_long_available*distance)
                
                self.brake_velocity[x] = v
                self.brake_a_long[x] = b_a_long_available
                self.brake_a_lat[x] = a_lat

        self.brake_velocity = self.shift_list(self.brake_velocity)
        self.brake_a_long = self.shift_list(self.brake_a_long)
        self.brake_a_lat = self.shift_list(self.brake_a_lat)

    def get_accel_velocity(self):
        return self.accel_velocity

    def get_accel_a_long(self):
        return self.accel_a_long

    def get_accel_a_lat(self):
        return self.accel_a_lat

    def get_brake_velocity(self):
        return self.brake_velocity

    def get_brake_a_long(self):
        return self.brake_a_long

    def get_brake_a_lat(self):
        return self.brake_a_lat

    def get_velocity(self):
        return [min(accel_vel, brake_vel) for accel_vel, brake_vel in zip(self.accel_velocity, self.brake_velocity)]

    def get_a_lat(self):
        a_lat = []
        velocity = self.get_velocity()
        crv = self.track.get_crv()

        for i in range(len(self.accel_a_lat)):
            a_lat.append(0)
            if velocity[i] == self.accel_velocity[i]:
                a_lat[i] = self.accel_a_lat[i]
            else:
                a_lat[i] = self.brake_a_lat[i]
            
            a_lat[i] = a_lat[i] * sign(crv[i])
        
        return a_lat

    def get_a_long(self):
        a_long = []
        velocity = self.get_velocity()

        for i in range(len(self.accel_a_long)):
            a_long.append(0)
            if velocity[i] == self.accel_velocity[i]:
                a_long[i] = self.accel_a_long[i]
            else:
                a_long[i] = self.brake_a_long[i] * -1
        
        return a_long

    
        