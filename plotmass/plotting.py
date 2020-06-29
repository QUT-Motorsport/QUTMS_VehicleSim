import matplotlib.pyplot as plt, mpld3
import matplotlib.patches as patches
import matplotlib.patches as mpatches

def plot_MassLap_all_html(window_w, window_h, x, crv, velocity, a_lat, a_long):
    fig,a =  plt.subplots(3,2)
    graph_width = (((window_w - 1100) * (15 - 8.2)) / (1920 - 1100)) + 8.2
    graph_height = (((window_h - 500) * (15.5 - 13)) / (1080 - 500)) + 13
    fig.set_size_inches(graph_width, graph_height)

    a[0][0].set_title('Track Curvature', fontweight='bold')
    a[0][0].plot(x,crv)
    a[0][0].set_ylabel('Curvature')
    a[0][0].set_xlabel('Distance (m)')
    a[0][0].margins(x=0, y=0.05)
    
    a[0][1].set_title('Speed Around Track', fontweight='bold')
    a[0][1].plot(x,velocity)
    a[0][1].set_ylabel('Speed (m/s)')
    a[0][1].set_xlabel('Distance (m)')
    a[0][1].margins(x=0, y=0.05)

    a[1][0].set_title('Lateral Acceleration vs Time', fontweight='bold')
    a[1][0].plot(x,a_lat)
    a[1][0].set_ylabel('Acceleration (m/s^2)')
    a[1][0].set_xlabel('Distance (m)')
    a[1][0].margins(x=0, y=0.05)

    a[1][1].set_title('Longitudinal Acceleration vs Time', fontweight='bold')
    a[1][1].plot(x,a_long)
    a[1][1].set_ylabel('Acceleration (m/s^2)')
    a[1][1].set_xlabel('Distance (m)')
    a[1][1].margins(x=0, y=0.05)

    a[2][0].set_title('G-G Diagram')
    a[2][0].plot(a_lat, a_long,'.')
    a[2][0].set_ylabel('Longitudinal Acceleration (m/s^2)')
    a[2][0].set_xlabel('Lateral Acceleration (m/s^2)')
    a[2][0].margins(x=0.01, y=0.01)

    fig.delaxes(a[2][1])
    fig.subplots_adjust(top = 0.97, bottom = 0.05, right = 1, left = 0.05, hspace = 0.2, wspace = 0.2)

    html_text = mpld3.fig_to_html(fig)
    return html_text, fig

def ggboxes(a_lat, a_long, ax):
    # Find where the boundaries of the points in the graph lie
    xmax = max(a_lat)
    ymax = max(a_long)
    xmin = min(a_lat)
    ymin = min(a_long)
    # Draw boxes around each section, the barriers for each section is defined here: (page 1) https://optimumg.com/wp-content/uploads/2019/09/RCE-Assymetrical-Setup-Part1.pdf
    rect1 = patches.Rectangle((xmin, 0.25 * 9.81), (-0.25 * 9.81 - xmin), (ymax - 0.25 * 9.81), linewidth=3, edgecolor='c', facecolor='none')
    rect2 = patches.Rectangle((-0.25 * 9.81, 0.25 * 9.81), (0.5 * 9.81), (ymax - 0.25 * 9.81), linewidth=3, edgecolor='r', facecolor='none')
    rect3 = patches.Rectangle((0.25 * 9.81, 0.25 * 9.81), (xmax - 0.25 * 9.81), (ymax - 0.25 * 9.81), linewidth=3, edgecolor='c', facecolor='none')
    rect4 = patches.Rectangle((xmin, -0.25 * 9.81), (-0.25 * 9.81 - xmin), (0.5 * 9.81), linewidth=3, edgecolor='m', facecolor='none')
    rect5 = patches.Rectangle((-0.25 * 9.81, -0.25 * 9.81), (0.5 * 9.81), (0.5 * 9.81), linewidth=3, edgecolor='g', facecolor='none')
    rect6 = patches.Rectangle((0.25 * 9.81, -0.25 * 9.81), (xmax - 0.25 * 9.81), (0.5 * 9.81), linewidth=3, edgecolor='m', facecolor='none')
    rect7 = patches.Rectangle((xmin, ymin), (-0.25 * 9.81 - xmin), (-0.25 * 9.81 - ymin), linewidth=3, edgecolor='y', facecolor='none')
    rect8 = patches.Rectangle((-0.25 * 9.81, ymin), (0.5 * 9.81), (-0.25 * 9.81 - ymin), linewidth=3, edgecolor='b', facecolor='none')
    rect9 = patches.Rectangle((0.25 * 9.81, ymin), (xmax - 0.25 * 9.81), (-0.25 * 9.81 - ymin), linewidth=3, edgecolor='y', facecolor='none')
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    ax.add_patch(rect3)
    ax.add_patch(rect4)
    ax.add_patch(rect5)
    ax.add_patch(rect6)
    ax.add_patch(rect7)  
    ax.add_patch(rect8)
    ax.add_patch(rect9)

def gg_legend(a_lat, a_long):
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

def gg_colour_sorting(a_lat, a_long, colour):
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


def plot_MassLap_gg_html(window_w, window_h, x, crv, velocity, a_lat, a_long):

    # Plot figure and determine size
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    graph_size = (((window_h - 500) * (12 - 7)) / (1080 - 500)) + 7
    fig.set_size_inches(graph_size, graph_size - 1)

    # Title diagram and create legend
    ax.set_title('G-G Diagram')
    colour = gg_legend(a_lat, a_long)

    #ggboxes(a_lat, a_long, ax) # Create boxes around sections
    
    # Colour the plots based on the position of the plots
    bx, by, cx, cy, dx, dy, ex, ey, fx, fy, gx, gy, hx, hy, ix, iy, jx, jy = gg_colour_sorting(a_lat, a_long, colour)
    ax.plot(bx, by, 'c.', markersize = 4)
    ax.plot(cx, cy, 'r.', markersize = 4)
    ax.plot(dx, dy, 'c.', markersize = 4)
    ax.plot(ex, ey, 'm.', markersize = 4)
    ax.plot(fx, fy, 'g.', markersize = 4)
    ax.plot(gx, gy, 'm.', markersize = 4)
    ax.plot(hx, hy, 'y.', markersize = 4)
    ax.plot(ix, iy, 'b.', markersize = 4)
    ax.plot(jx, jy, 'y.', markersize = 4)
    ax.set_ylabel('Longitudinal Acceleration (m/s^2)')
    ax.set_xlabel('Lateral Acceleration (m/s^2)')
    ax.margins(x=0.1, y=0.1)
      

    html_text = mpld3.fig_to_html(fig)
    return html_text, fig

def plot_MassLap_SpeedCurvature_html(window_w, window_h, x, crv, velocity):
    # Plot figure and determine size
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    graph_size = (((window_h - 500) * (12 - 7)) / (1080 - 500)) + 7
    fig.set_size_inches(graph_size, graph_size - 1)

    # Title diagram and create legend
    ax.set_title('Speed v Curvature')
    
    # Colour the plots based on the position of the plots
    ax.plot(x, [abs(i * 100) for i in crv], label='Absolute Curvature * 100')
    ax.plot(x, velocity, label='Speed (m/s)')
    ax.legend()
    ax.set_xlabel('Distance (m)')
    ax.margins(x=0.1, y=0.1)
    
      

    html_text = mpld3.fig_to_html(fig)
    return html_text, fig