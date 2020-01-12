from math import *

def shift_list(master_list, start_position, end_position, offset):
    primary_list = master_list[start_position + offset:len(master_list)]
    secondary_list = master_list[0:end_position + offset + 1]
    master_list = primary_list + secondary_list
    return master_list

def braking(g, m, P, p, A, Cd, mu, Cl, peak_loc, x_array, lat_velocity, crv_array, start_position, end_position, offset, array_length):
    number_of_peaks = len(peak_loc)
    x = array_length
    y = 0
    s = x_array
    brake_velocity = []
    brake_a_long = []
    brake_a_lat = []

    for i in range(array_length):
        brake_velocity.append(0)
        brake_a_long.append(0)
        brake_a_lat.append(0)

    for nn in range(number_of_peaks, -1, -1):
        if nn == number_of_peaks:
            start_point = array_length - 1
            end_point = peak_loc[number_of_peaks - 1] + 1
        elif nn == 0:
            start_point = peak_loc[0]
            end_point = 0
        else:
            start_point = peak_loc[nn]
            end_point = peak_loc[nn - 1] + 1

        for n in range(start_point, end_point - 1, -1):
            x -= 1
            if n == peak_loc[0]:
                v = lat_velocity[peak_loc[0]]
                b_a_long_available = 0
                N = m*g+(0.5*p*lat_velocity[n]**2*-Cl*A)
                a_resultant = (mu*N)/m
                a_lat = a_resultant
            elif n == start_point:
                v = lat_velocity[start_point]
                b_a_long_available = 0
                N = m*g+(0.5*p*lat_velocity[n]**2*-Cl*A)
                a_resultant = (mu*N)/m
                a_lat = a_resultant
            else:
                distance = s[n+1]-s[n]
                N = m*g+(0.5*p*brake_velocity[x+1]**2*-Cl*A)
                a_lat = brake_velocity[x+1]**2*crv_array[n]
                a_resultant = (mu*N)/m
                if a_lat>a_resultant:
                    a_lat = a_resultant
                b_a_long_available = sqrt(a_resultant**2-a_lat**2)
                v = sqrt((brake_velocity[x+1])**2+2*b_a_long_available*distance)
            
            brake_velocity[x] = v
            brake_a_long[x] = b_a_long_available
            brake_a_lat[x] = a_lat

    brake_velocity = shift_list(brake_velocity, start_position, end_position, offset)
    brake_a_long = shift_list(brake_a_long, start_position, end_position, offset)
    brake_a_lat = shift_list(brake_a_lat, start_position, end_position, offset)

    # Debug
    # print("Vel: " + str(brake_velocity[0]) + ' ' + str(brake_velocity[len(brake_velocity)-1]) + ' ' + str(len(brake_velocity)))
    # print("Long: " + str(brake_a_long[0]) + ' ' + str(brake_a_long[len(brake_a_long)-1]) + ' ' + str(len(brake_a_long)))
    # print("Lat: " + str(brake_a_lat[0]) + ' ' + str(brake_a_lat[len(brake_a_lat)-1]) + ' ' + str(len(brake_a_lat)))

    return brake_velocity, brake_a_long, brake_a_lat

