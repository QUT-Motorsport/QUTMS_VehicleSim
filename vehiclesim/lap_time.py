from datetime import *

def lap_time(velocity, pos_list):
    lap_time = 0
    distance = []
    time = []

    for i in range(len(velocity)):
        distance.append(0)
        time.append(0)
        if i != 0:
            distance[i] = pos_list[i] - pos_list[i - 1]
            time[i] = distance[i]/velocity[i]
        lap_time += time[i]

    return str(timedelta(seconds=round(lap_time, 2)))[:-4]


    