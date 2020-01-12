from numpy import *

def slip_angle(forward_velocity, lateral_velocity):
	slip_angles = []
	for i in range(forward_velocity):
		slip_angles.append(arctan(lateral_velocity/forward_velocity)) * -1
	return slip_angles