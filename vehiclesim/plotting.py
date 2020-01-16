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
    xmax = max(a_lat)
    ymax = max(a_long)
    xmin = min(a_lat)
    ymin = min(a_long)
    rect1 = patches.Rectangle((xmin, 0.25 * 9.81), (-0.25 * 9.81 - xmin), (ymax - 0.25 * 9.81), linewidth=3, edgecolor='r', facecolor='none')
    rect2 = patches.Rectangle((-0.25 * 9.81, 0.25 * 9.81), (0.5 * 9.81), (ymax - 0.25 * 9.81), linewidth=3, edgecolor='#6a0dad', facecolor='none')
    rect3 = patches.Rectangle((0.25 * 9.81, 0.25 * 9.81), (xmax - 0.25 * 9.81), (ymax - 0.25 * 9.81), linewidth=3, edgecolor='g', facecolor='none')
    rect4 = patches.Rectangle((xmin, -0.25 * 9.81), (-0.25 * 9.81 - xmin), (0.5 * 9.81), linewidth=3, edgecolor='#ffa500', facecolor='none')
    rect5 = patches.Rectangle((-0.25 * 9.81, -0.25 * 9.81), (0.5 * 9.81), (0.5 * 9.81), linewidth=3, edgecolor='k', facecolor='none')
    rect6 = patches.Rectangle((0.25 * 9.81, -0.25 * 9.81), (xmax - 0.25 * 9.81), (0.5 * 9.81), linewidth=3, edgecolor='c', facecolor='none')
    rect7 = patches.Rectangle((xmin, ymin), (-0.25 * 9.81 - xmin), (-0.25 * 9.81 - ymin), linewidth=3, edgecolor='b', facecolor='none')
    rect8 = patches.Rectangle((-0.25 * 9.81, ymin), (0.5 * 9.81), (-0.25 * 9.81 - ymin), linewidth=3, edgecolor='#654321', facecolor='none')
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

    for i in range(len(a_lat)): 
        if a_lat[i] > 0.25 * 9.8:
            if a_long[i] < -0.25 * 9.8: 
                yellow += 1 # Trail braking into left corner 
                colour.append(8)
            elif -0.25 * 9.8 <= a_long[i] <= 0.25 * 9.8: 
                cyan += 1 # Pure left cornering 
                colour.append(5)
            elif a_long[i] > 0.25 * 9.8: 
                green += 1 # Combined acceleration out of a left turn
                colour.append(2)
        elif -0.25 * 9.8 <= a_lat[i] <= 0.25 * 9.8:
            if a_long[i] < -0.25 * 9.8: 
                brown += 1 # Pure braking 
                colour.append(7)
            elif -0.25 * 9.8 <= a_long[i] <= 0.25 * 9.8: 
                black += 1 # Center
                colour.append(4)
            elif a_long[i] > 0.25 * 9.8: 
                purple += 1 # Pure acceleration 
                colour.append(1)
        elif a_lat[i] < -0.25 * 9.8: 
            if a_long[i] < -0.25 * 9.8: 
                blue += 1 # Trail braking going into right corner
                colour.append(6)
            elif -0.25 * 9.8 <= a_long[i] <= 0.25 * 9.8: 
                orange += 1 # Pure right cornering
                colour.append(3)
            elif a_long[i] > 0.25 * 9.8: 
                red += 1 # Combined acceleration out of a right turn
                colour.append(0)

    red = round(((red / len(a_lat))*100), 2)
    purple = round(((purple / len(a_lat))*100), 2)
    green = round(((green / len(a_lat))*100), 2)
    orange = round(((orange / len(a_lat))*100), 2)
    black = round(((black / len(a_lat))*100), 2)
    cyan = round(((cyan / len(a_lat))*100), 2)
    blue = round(((blue / len(a_lat))*100), 2)
    brown = round(((brown / len(a_lat))*100), 2)
    yellow = round(((yellow / len(a_lat))*100), 2)

    red_label = 'Accel right {}%'.format(red)
    purple_label = 'Pure accel {}%'.format(purple)
    green_label = 'Accel left {}%'.format(green)
    orange_label = 'Right cornering {}%'.format(orange)
    black_label= 'Center {}%'.format(black)
    cyan_label= 'Left cornering {}%'.format(cyan)
    blue_label= 'Braking right {}%'.format(blue)
    brown_label= 'Pure braking {}%'.format(brown)
    yellow_label= 'Braking left {}%'.format(yellow)

    red_patch = mpatches.Patch(color='c', label=red_label)
    purple_patch = mpatches.Patch(color='r', label=purple_label) 
    green_patch = mpatches.Patch(color='c', label=green_label)
    orange_patch = mpatches.Patch(color='m', label=orange_label)
    black_patch = mpatches.Patch(color='g', label=black_label)
    cyan_patch = mpatches.Patch(color='m', label=cyan_label)
    blue_patch = mpatches.Patch(color='y', label=blue_label)
    brown_patch = mpatches.Patch(color='b', label=brown_label)
    yellow_patch = mpatches.Patch(color='y', label=yellow_label)
    plt.legend(handles=[red_patch, purple_patch, green_patch, orange_patch, black_patch, cyan_patch, blue_patch, brown_patch, yellow_patch], loc = 'lower left')
    
    return colour

def gg_colour_sorting(a_lat, a_long, colour):

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
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    graph_size = (((window_h - 500) * (12 - 7)) / (1080 - 500)) + 7
    fig.set_size_inches(graph_size, graph_size - 1)

    ax.set_title('G-G Diagram')
    #ggboxes(a_lat, a_long, ax)
    colour = gg_legend(a_lat, a_long)
    
    bx, by, cx, cy, dx, dy, ex, ey, fx, fy, gx, gy, hx, hy, ix, iy, jx, jy = gg_colour_sorting(a_lat, a_long, colour)
    ax.plot(a_lat, a_long, 'b.')
    ax.plot(bx, by, 'c.')
    ax.plot(cx, cy, 'r.')
    ax.plot(dx, dy, 'c.')
    ax.plot(ex, ey, 'm.')
    ax.plot(fx, fy, 'g.')
    ax.plot(gx, gy, 'm.')
    ax.plot(hx, hy, 'y.')
    ax.plot(ix, iy, 'b.')
    ax.plot(jx, jy, 'y.')
    ax.set_ylabel('Longitudinal Acceleration (m/s^2)')
    ax.set_xlabel('Lateral Acceleration (m/s^2)')
    ax.margins(x=0.1, y=0.1)
      

    html_text = mpld3.fig_to_html(fig)
    return html_text, fig

def plot_MassLap_SpeedCurvature_html():
    pass

def plot_everything(x, crv, velocity, a_lat, a_long):
    fig,a =  plt.subplots(2,2)

    fig.canvas.set_window_title('plotMassLapSim')
    fig.set_size_inches(15, 9)

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

    plt.show()

def plotting_curvature(x,crv):
    plt.figure('plotting_curvature')
    plt.plot(x,crv)
    plt.ylabel('Curvature')
    plt.title('Track Curvature')
    plt.xlabel('Distance (m)')
    plt.show()
    
def plotting_velocity(x,velocity):
    plt.figure('plotting_velocity')
    plt.plot(x,velocity)
    plt.ylabel('Speed (m/s)')
    plt.title('Speed Around Track')
    plt.xlabel('Distance (m)')
    plt.show()

def plotting_a_lat(x,a_lat):
    plt.figure('plotting_a_lat')
    plt.plot(x,a_lat)
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Lateral Acceleration vs Time')
    plt.xlabel('Distance (m)')
    plt.show()

def plotting_a_long(x,a_long):
    plt.figure('plotting_velocity')
    plt.plot(x,a_long)
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Longitudinal Acceleration vs Time')
    plt.xlabel('Distance (m)')
    plt.show()

def GG(a_lat, a_long):
    plt.figure('G-G Diagram')
    plt.plot(a_lat, a_long,'.')
    plt.ylabel('Longitudinal Acceleration (m/s^2)')
    plt.title('G-G Diagram')
    plt.xlabel('Lateral Acceleration (m/s^2)')
    plt.margins(x=0.01, y=0.01)
    plt.show()