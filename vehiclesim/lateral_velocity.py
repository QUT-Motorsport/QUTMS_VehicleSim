from scipy.signal import find_peaks
import pandas as pd
import numpy
from math import *

def nthroot(num, root):
    answer = num ** (1/root)
    return answer

def lateral_velocity(g, m, P, p, A, Cd, mu, Cl, array_length, crv_array):
    radius = []
    for entry in crv_array:
        radius.append(1/entry)       
    top_speed = nthroot((2*P)/(p*Cd*A),3)
    lat_velocity = []
    inv_lat_velocity = []
    for n in radius:
        if 0.5*n*p*-Cl*A*mu > m:
            vel = top_speed
        else:
            vel = sqrt((n*mu*m*g)/(m-0.5*n*p*-Cl*A*mu))
            if vel>top_speed:
               vel=top_speed
        lat_velocity.append(vel)
        inv_lat_velocity.append(1/vel)
    peak_loc_values = find_peaks(inv_lat_velocity)
    peak_loc = peak_loc_values[0]
    return lat_velocity, peak_loc




