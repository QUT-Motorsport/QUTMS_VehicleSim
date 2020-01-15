import matplotlib.pyplot as plt, mpld3

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

def plot_MassLap_gg_html(window_w, window_h, x, crv, velocity, a_lat, a_long):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    graph_size = (((window_h - 500) * (12 - 7)) / (1080 - 500)) + 7
    fig.set_size_inches(graph_size, graph_size - 1)

    ax.set_title('G-G Diagram')
    ax.plot(a_lat, a_long,'.')
    ax.set_ylabel('Longitudinal Acceleration (m/s^2)')
    ax.set_xlabel('Lateral Acceleration (m/s^2)')
    ax.margins(x=0.01, y=0.01)

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