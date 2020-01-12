from numpy import sign, append

def lat_long(accel_lat, accel_long, brake_lat, brake_long, accel_velocity, velocity, crv):
    a_lat = []
    a_long = []

    for i in range(len(accel_lat)):
        a_lat.append(0)
        a_long.append(0)
        if velocity[i] == accel_velocity[i]:
            a_lat[i] = accel_lat[i]
            a_long[i] = accel_long[i]
        else:
            a_lat[i] = brake_lat[i]
            a_long[i] = brake_long[i] * -1
        
        a_lat[i] = a_lat[i] * sign(crv[i])

    return a_lat, a_long