import matplotlib.pyplot as plt, mpld3
import matplotlib.patches as patches
import matplotlib.patches as mpatches

class GG_Diagram:

    def __init__(self, window_w, window_h, a_lat, a_long):

        # Plot figure and determine size
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        graph_size = (((window_h - 500) * (12 - 7)) / (1080 - 500)) + 7
        self.fig.set_size_inches(graph_size, graph_size - 1)

        # Title diagram and create legend
        self.ax.set_title('G-G Diagram')
        colour = self.gg_legend(a_lat, a_long)

        bx, by, cx, cy, dx, dy, ex, ey, fx, fy, gx, gy, hx, hy, ix, iy, jx, jy = self.gg_colour_sorting(a_lat, a_long, colour)
        self.ax.plot(bx, by, 'c.', markersize = 4)
        self.ax.plot(cx, cy, 'r.', markersize = 4)
        self.ax.plot(dx, dy, 'c.', markersize = 4)
        self.ax.plot(ex, ey, 'm.', markersize = 4)
        self.ax.plot(fx, fy, 'g.', markersize = 4)
        self.ax.plot(gx, gy, 'm.', markersize = 4)
        self.ax.plot(hx, hy, 'y.', markersize = 4)
        self.ax.plot(ix, iy, 'b.', markersize = 4)
        self.ax.plot(jx, jy, 'y.', markersize = 4)
        self.ax.set_ylabel('Longitudinal Acceleration (m/s^2)')
        self.ax.set_xlabel('Lateral Acceleration (m/s^2)')
        self.ax.margins(x=0.1, y=0.1)

    def plot(self):
        return self.fig

    def gg_legend(self, a_lat, a_long):
        # Initialise lists and counter values for each GG diagram section
        colour = []
        red = 0 
        purple = 0
        green = 0
        orange = 0
        black = 0
        cyan = 0
        blue = 0 
        brown = 0
        yellow = 0
        # For each point in the graph define where it lies
        # If a point is in a given section a number is appended into a list which is later used to colour the diagram according to the GG diagram sections
        # The counters are increased to determine what % of the time the car is in a certain section  
        for i in range(len(a_lat)): 
            if a_lat[i] > 0.25 * 9.8:
                # Trail braking into left corner
                if a_long[i] < -0.25 * 9.8: 
                    yellow += 1 
                    colour.append(8)
                # Pure left cornering 
                elif -0.25 * 9.8 <= a_long[i] <= 0.25 * 9.8: 
                    cyan += 1 
                    colour.append(5)
                # Combined acceleration out of a left turn
                elif a_long[i] > 0.25 * 9.8: 
                    green += 1 
                    colour.append(2)
            elif -0.25 * 9.8 <= a_lat[i] <= 0.25 * 9.8:
                # Pure braking
                if a_long[i] < -0.25 * 9.8: 
                    brown += 1  
                    colour.append(7)
                # Center
                elif -0.25 * 9.8 <= a_long[i] <= 0.25 * 9.8: 
                    black += 1 
                    colour.append(4)
                # Pure acceleration
                elif a_long[i] > 0.25 * 9.8: 
                    purple += 1  
                    colour.append(1)
            elif a_lat[i] < -0.25 * 9.8: 
                # Trail braking going into right corner
                if a_long[i] < -0.25 * 9.8: 
                    blue += 1 
                    colour.append(6)
                # Pure right cornering
                elif -0.25 * 9.8 <= a_long[i] <= 0.25 * 9.8: 
                    orange += 1 
                    colour.append(3)
                # Combined acceleration out of a right turn
                elif a_long[i] > 0.25 * 9.8: 
                    red += 1 
                    colour.append(0)

        # Find percentage of time car spends in each section
        red = round(((red / len(a_lat))*100), 2)
        purple = round(((purple / len(a_lat))*100), 2)
        green = round(((green / len(a_lat))*100), 2)
        orange = round(((orange / len(a_lat))*100), 2)
        black = round(((black / len(a_lat))*100), 2)
        cyan = round(((cyan / len(a_lat))*100), 2)
        blue = round(((blue / len(a_lat))*100), 2)
        brown = round(((brown / len(a_lat))*100), 2)
        yellow = round(((yellow / len(a_lat))*100), 2)

        # Create a legend with percentage of time car spends in each section
        red_label = 'Accel Right {}%'.format(red)
        purple_label = 'Pure Accel {}%'.format(purple)
        green_label = 'Accel Left {}%'.format(green)
        orange_label = 'Right Cornering {}%'.format(orange)
        black_label= 'Center {}%'.format(black)
        cyan_label= 'Left Cornering {}%'.format(cyan)
        blue_label= 'Braking Right {}%'.format(blue)
        brown_label= 'Pure Braking {}%'.format(brown)
        yellow_label= 'Braking Left {}%'.format(yellow)

        red_patch = mpatches.Patch(color='c', label=red_label)
        purple_patch = mpatches.Patch(color='r', label=purple_label) 
        green_patch = mpatches.Patch(color='c', label=green_label)
        orange_patch = mpatches.Patch(color='m', label=orange_label)
        black_patch = mpatches.Patch(color='g', label=black_label)
        cyan_patch = mpatches.Patch(color='m', label=cyan_label)
        blue_patch = mpatches.Patch(color='y', label=blue_label)
        brown_patch = mpatches.Patch(color='b', label=brown_label)
        yellow_patch = mpatches.Patch(color='y', label=yellow_label)
        # Position the labels 
        plt.legend(handles=[red_patch, purple_patch, green_patch, orange_patch, black_patch, cyan_patch, blue_patch, brown_patch, yellow_patch], loc = 'lower left')
        
        return colour

    def gg_colour_sorting(self, a_lat, a_long, colour):
        # Create lists for each of the individual section
        # Each section has two lists - one for each of the lateral and longitudinal positions of the car when it is in a given GG diagram section
        accel_right_lat = []
        accel_right_long = []
        pure_accel_lat = [] 
        pure_accel_long = [] 
        accel_left_lat = [] 
        accel_left_long = [] 
        pure_right_lat = [] 
        pure_right_long = [] 
        center_lat = [] 
        center_long = [] 
        pure_left_lat = [] 
        pure_left_long = [] 
        brake_right_lat = [] 
        brake_right_long = [] 
        pure_brake_lat = [] 
        pure_brake_long = [] 
        brake_left_lat = [] 
        brake_left_long = []

        # For all the coordinates found if the car is in a given section append the coordinates to the appropriate list
        for i in range(len(colour)):
            if colour[i] == 0:
                accel_right_lat.append(a_lat[i])
                accel_right_long.append(a_long[i])
            elif colour[i] == 1:
                pure_accel_lat.append(a_lat[i])
                pure_accel_long.append(a_long[i])
            elif colour[i] == 2:
                accel_left_lat.append(a_lat[i])
                accel_left_long.append(a_long[i])
            elif colour[i] == 3:
                pure_right_lat.append(a_lat[i])
                pure_right_long.append(a_long[i])
            elif colour[i] == 4:
                center_lat.append(a_lat[i])
                center_long.append(a_long[i])
            elif colour[i] == 5:
                pure_left_lat.append(a_lat[i])
                pure_left_long.append(a_long[i])
            elif colour[i] == 6:
                brake_right_lat.append(a_lat[i])
                brake_right_long.append(a_long[i])
            elif colour[i] == 7:
                pure_brake_lat.append(a_lat[i])
                pure_brake_long.append(a_long[i])
            elif colour[i] == 8:
                brake_left_lat.append(a_lat[i])
                brake_left_long.append(a_long[i])

        return accel_right_lat, accel_right_long, pure_accel_lat, pure_accel_long, accel_left_lat, accel_left_long, pure_right_lat, pure_right_long, center_lat, center_long, pure_left_lat, pure_left_long, brake_right_lat, brake_right_long, pure_brake_lat, pure_brake_long, brake_left_lat, brake_left_long

