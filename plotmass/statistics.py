from datetime import timedelta

class Statistics:

    def __init__(self, velocity, dist):

        # Calculate time
        self.lap_time = 0
        dist_travelled = []
        self.time = []

        for i in range(len(velocity)):
            dist_travelled.append(0)
            self.time.append(0)
            if i != 0:
                dist_travelled[i] = dist[i] - dist[i - 1]
                self.time[i] = dist_travelled[i]/velocity[i]
            self.lap_time += self.time[i]

        self.fastest_lap = str(timedelta(seconds=round(self.lap_time, 2)))[:-4]

        # Aggregated time
        self.agg_time = [None] * len(self.time)

        for num, value in enumerate(self.time):
            if num == 0:
                self.agg_time[num] = value
            else:
                self.agg_time[num] = self.agg_time[num-1] + value

        print(self.agg_time)

        # Calculate max and min speeds in km/h
        self.max_speed = round(max(velocity) * 3.6, 2)
        self.min_speed = round(min(velocity) * 3.6, 2)

    def get_t(self):
        return self.time

    def get_time(self):
        return self.get_t()

    def get_agg_time(self):
        return self.agg_time

    def get_fastest_lap(self):
        return self.fastest_lap

    def get_lap_time(self):
        return self.lap_time

    def get_max_speed(self):
        return self.max_speed
    
    def get_min_speed(self):
        return self.min_speed