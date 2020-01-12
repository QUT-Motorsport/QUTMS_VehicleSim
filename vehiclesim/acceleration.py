from scipy.signal import find_peaks
import pandas as pd
import numpy
from math import *
from numpy import *

def shift_list(master_list, start_position, end_position, offset):
    primary_list = master_list[start_position + offset:len(master_list)]
    secondary_list = master_list[0:end_position + offset + 1]
    master_list = primary_list + secondary_list
    return master_list

def acceleration(g, m, P, p, A, Cd, mu, Cl, peak_loc, x_array, lat_velocity, crv_array, start_position, end_position, offset, array_length):
    number_of_peaks = len(peak_loc)
    s = x_array
    x = -1
    accel_velocity = []
    accel_a_long = []
    accel_a_lat = []
    is_accel = False

    for nn in range(0, number_of_peaks + 1):

        if nn == 0:
            start_point = 0
            end_point = peak_loc[0] - 1
        elif nn == number_of_peaks:
            start_point = peak_loc[nn - 1]
            end_point = len(lat_velocity)
        else:
            start_point = peak_loc[nn - 1]
            end_point = peak_loc[nn] - 1

        for n in range(start_point, end_point + 1):
            x += 1
            if n == 0:
                v = lat_velocity[0]
                N = m*g+(0.5*p*lat_velocity[0]**2*-Cl*A)
                a_resultant = (mu*N/m)
                a_a_long_available = 0
                a_lat = a_resultant
            elif n == start_point and is_accel and accel_velocity[x - 1] < lat_velocity[peak_loc[nn - 1]]:
                v = accel_velocity[x - 1]
                a_a_long_available = accel_a_long[x - 1]
                a_lat = accel_a_lat[x - 1]
            elif n == start_point:
                v = lat_velocity[start_point]
                N = m*g+(0.5*p*lat_velocity[n]**2*-Cl*A)
                a_resultant = (mu*N)/m
                a_a_long_available = 0
                a_lat = a_resultant
            else:
                try:
                    distance = s[n] - s[n - 1]
                    N = m*g+(0.5*p*accel_velocity[x - 1]**2*-Cl*A)              
                    a_lat = accel_velocity[x - 1]**2*crv_array[n]
                except:
                    break
                a_resultant = (mu*N)/m
                if a_lat > a_resultant:
                    a_lat = a_resultant
                GL_a_long_available = sqrt(a_resultant**2-a_lat**2)
                try:
                    PL_a_long_available = ((P/accel_velocity[x-1])-(0.5*p*(accel_velocity[x-1])**2*Cd*A))/m
                except ZeroDivisionError:
                    PL_a_long_available = 0
                a_a_long_available = minimum(GL_a_long_available, PL_a_long_available)
                v = sqrt((accel_velocity[x-1])**2+2*a_a_long_available*distance)

            if is_accel == False:
                is_accel = True
            
            accel_velocity.append(v)
            accel_a_long.append(a_a_long_available)
            accel_a_lat.append(a_lat)
    
    accel_velocity = shift_list(accel_velocity, start_position, end_position, offset)
    accel_a_long = shift_list(accel_a_long, start_position, end_position, offset)
    accel_a_lat = shift_list(accel_a_lat, start_position, end_position, offset)

    return accel_velocity, accel_a_long, accel_a_lat