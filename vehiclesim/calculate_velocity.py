from numpy import *

def calculate_velocity(accel_velocity, brake_velocity):
    velocity = []

    for i in range(len(accel_velocity)):
        velocity.append(minimum(accel_velocity[i], brake_velocity[i]))

    return velocity