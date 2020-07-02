from .track import Track
from .constants import Constants
from .lateral_velocity import LateralVelocity
from .momentum import Momentum
from .statistics import Statistics
from .gg_diagram import GG_Diagram

import pickle
import matplotlib.pyplot as plt, mpld3

class PlotMassSimulation:
    """Implementation of a Plot Mass Lap Simulation

    Calculates the velocity of a 1D object of mass around a track
    """

    def __init__(self, mat_file, crv_name, window_w, window_h, m=0, P=0, p=0, A=0, Cd=0, mu=0, Cl=0, g=9.81, constants=[]):
        """Constructs an instance of the Plot Mass model

        Populates velocity arrays from inputted data with mathematical models
        """

        # Make parameters attributes
        self.window_h = window_h
        self.window_w = window_w

        # Populate constants
        if m == 0 and P == 0 and g == 9.81 and constants != []:
            vehicle = Constants(item=constants)
        else:
            vehicle = Constants(g, m, P, p, A, Cd, mu, Cl)

        # Fetch track data from .mat file
        track = Track(mat_file, crv_name, 'x')
        self.track = track.get_track()
        
        # Calculate Maximum Lateral Velocity
        latVel = LateralVelocity(vehicle, track)
        self.lat_velocity = latVel.get_lat_velocity()
        self.peak_loc = latVel.get_peak_loc()

        # Calculate Acceleration and Deacceleration
        self.momentum = Momentum(vehicle, track, self.peak_loc, self.lat_velocity)
        self.momentum.calc_accel()
        self.momentum.calc_deaccel()

        # Calculate Expected Velocity
        self.velocity = self.momentum.get_velocity()
        self.a_lat = self.momentum.get_a_lat()
        self.a_long = self.momentum.get_a_long()

        # Fetch statistics of lap
        self.statistics = Statistics(self.velocity, track.get_x())

    def output(self):
        """Useful for debugging

        Print statements of class attributes to compare values
        """
        pass

    def pickle(self, fig, fig_name):
        """Saves statistics & graphs to file system
        """

        # pickle the 'image' to be called later to download
        pickle.dump(fig, open(fig_name, "wb"))

        # pickle the core stats to download
        pickle_stats = {}
        pickle_stats["velocity"] = self.velocity
        pickle_stats["time"] = self.statistics.get_t()
        pickle_stats["long_accel"] = self.a_long
        pickle.dump(pickle_stats, open("statistics.p", "wb"))

    def plot(self):
        """Return a matplotlib figure

        Primary view of all preliminary graphs
        View curvature, speed, lat & long forces
        """

        fig,a =  plt.subplots(3,2)
        graph_width = (((self.window_w - 1100) * (15 - 8.2)) / (1920 - 1100)) + 8.2
        graph_height = (((self.window_h - 500) * (15.5 - 13)) / (1080 - 500)) + 13
        fig.set_size_inches(graph_width, graph_height)

        a[0][0].set_title('Track Curvature', fontweight='bold')
        a[0][0].plot(self.track['x_array'], self.track['crv'])
        a[0][0].set_ylabel('Curvature')
        a[0][0].set_xlabel('Distance (m)')
        a[0][0].margins(x=0, y=0.05)
        
        a[0][1].set_title('Speed Around Track', fontweight='bold')
        a[0][1].plot(self.track['x_array'], self.velocity)
        a[0][1].set_ylabel('Speed (m/s)')
        a[0][1].set_xlabel('Distance (m)')
        a[0][1].margins(x=0, y=0.05)

        a[1][0].set_title('Lateral Acceleration vs Time', fontweight='bold')
        a[1][0].plot(self.track['x_array'], self.a_lat)
        a[1][0].set_ylabel('Acceleration (m/s^2)')
        a[1][0].set_xlabel('Distance (m)')
        a[1][0].margins(x=0, y=0.05)

        a[1][1].set_title('Longitudinal Acceleration vs Time', fontweight='bold')
        a[1][1].plot(self.track['x_array'], self.a_long)
        a[1][1].set_ylabel('Acceleration (m/s^2)')
        a[1][1].set_xlabel('Distance (m)')
        a[1][1].margins(x=0, y=0.05)

        a[2][0].set_title('G-G Diagram')
        a[2][0].plot(self.a_lat, self.a_long,'.')
        a[2][0].set_ylabel('Longitudinal Acceleration (m/s^2)')
        a[2][0].set_xlabel('Lateral Acceleration (m/s^2)')
        a[2][0].margins(x=0.01, y=0.01)

        fig.delaxes(a[2][1])
        fig.subplots_adjust(top = 0.97, bottom = 0.05, right = 1, left = 0.05, hspace = 0.2, wspace = 0.2)

        return fig

    def plot_html(self):
        """Return a string

        Generates an mpld3 plot in html tags to display
        the primary plot within a template
        """
        return mpld3.fig_to_html(self.plot())

    def plot_gg(self):
        """Return a matplotlib figure

        Creates an instance of a GG Diagram, and generates
        the required plot
        """
        gg = GG_Diagram(self.window_w, self.window_h, self.a_lat, self.a_long)
        return gg.plot()

    def plot_gg_html(self):
        """Return a string

        Generates an mpld3 plot in html tags to display
        the complete colour-coded GG Diagram
        """
        return mpld3.fig_to_html(self.plot_gg())

    def plot_speed_curvature(self):
        """Return a matplotlib plot

        Creates an instance of an experimental Speed v Curvature Diagram, 
        and generates the required plot
        """

        # Plot figure and determine size
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        graph_size = (((self.window_h - 500) * (12 - 7)) / (1080 - 500)) + 7
        fig.set_size_inches(graph_size, graph_size - 1)

        # Title diagram
        ax.set_title('Speed v Curvature')
        
        # Populate data on the axis'
        ax.plot(self.track['x_array'], [abs(i * 100) for i in self.track['crv']], label='Absolute Curvature * 100')
        ax.plot(self.track['x_array'], self.velocity, label='Speed (m/s)')
        ax.legend()
        ax.set_xlabel('Distance (m)')
        ax.margins(x=0.1, y=0.1)
        return fig

    def plot_speed_curvature_html(self):
        """Return a string

        Generates an mpld3 plot in html tags to display
        the Speed v Curvature Diagram
        """
        return mpld3.fig_to_html(self.plot_speed_curvature())
        
    def get_fastest_lap(self):
        """Return a string

        Generates a complete string with the simulated time taken to complete
        a lap of the inputted data array
        """
        return self.statistics.get_fastest_lap()
