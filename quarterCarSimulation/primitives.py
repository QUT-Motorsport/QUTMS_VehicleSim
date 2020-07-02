from numpy import pi
from math import sqrt

class Primitives:
    """
    Stores and return values needed for output and calculations of QCar Model
    For values that are not arrays, and require one single instance
    """

    def __init__(self, sprung_mass, unsprung_mass, wheel_rate, spring_rate, damping_ratio_compression, rounding=10):
        self.sprung_mass = sprung_mass
        self.unsprung_mass = unsprung_mass
        self.wheel_rate = wheel_rate
        self.spring_rate = spring_rate
        self.damping_ratio_compression = damping_ratio_compression
        self.rounding = rounding

        self.headings = ["Sprung Mass Natural Frequency (Hz)",
                "Sprung Mass Damped Frequency (Hz)",
                "Unsprung Mass Natural Frequency",
                "Unsprung Mass Damped Frequency",
                "Eigen Values and Eigen Vectors of the Quarter Car"]

    # Calculations

    def get_sprung_mass_natural_frequency(self):
        """Returns an integer
        
        Calculates Sprung Mass Natural Frequency

        Resources:
        https://www.ijera.com/papers/vol9no3/Series-3/K0903036064%20.pdf
        https://www.drtuned.com/tech-ramblings/2017/10/2/spring-rates-suspension-frequencies
        https://core.ac.uk/download/pdf/14697847.pdf
        http://www.kaztechnologies.com/wp-content/uploads/2015/06/A-Guide-To-Your-Dampers-Chapter-from-FSAE-Book-by-Jim-Kasprzak-Updated.pdf
        https://core.ac.uk/download/pdf/82554529.pdf
        https://journals.sagepub.com/doi/pdf/10.1177/1687814016648638
        https://iopscience.iop.org/article/10.1088/1742-6596/1273/1/012073/pdf
        """
        return round(0.5 * (1.0/pi) * sqrt(self.spring_rate / self.sprung_mass), self.rounding)

    def get_sprung_mass_damped_frequency(self):
        """Returns an integer
        
        Calculate Sprung Mass Damped Frequency from Natural Frequency

        Resources:
        https://en.wikipedia.org/wiki/Vibration#Free_vibration_with_damping
        """
        return round(self.get_sprung_mass_natural_frequency() * sqrt(1 - (self.damping_ratio_compression**2)), self.rounding)

    def get_unsprung_mass_natural_frequency(self):
        """Needs comment Maclayne with resource reference
        """
        return round(1 / (2 * pi) * sqrt(self.wheel_rate + self.spring_rate / self.unsprung_mass), self.rounding)

    def get_unsprung_mass_damped_frequency(self):
        """Needs comment Maclayne with resource reference
        """
        return round(self.get_unsprung_mass_natural_frequency() * sqrt(1 - (self.damping_ratio_compression**2)), self.rounding)

    def get_eigen_values(self):
        return 5

    # Display format methods

    def get_headings(self):
        return self.headings

    def set_headings(self, headings):
        self.headings = headings

    def get_values(self):
        return [self.get_sprung_mass_natural_frequency(),
              self.get_sprung_mass_damped_frequency(),
              self.get_unsprung_mass_natural_frequency(),
              self.get_unsprung_mass_damped_frequency(),
              self.get_eigen_values()]

    # Attributes

    def get_sprung_mass(self):
        return self.sprung_mass
    
    def set_sprung_mass(self, sprung_mass):
        self.sprung_mass = sprung_mass

    def get_unsprung_mass(self):
        return self.unsprung_mass

    def set_unsprung_mass(self, unsprung_mass):
        self.unsprung_mass = unsprung_mass

    def get_wheel_rate(self):
        return self.get_wheel_rate

    def set_wheel_rate(self, wheel_rate):
        self.wheel_rate = wheel_rate

    def get_spring_rate(self):
        return self.spring_rate

    def set_spring_rate(self, spring_rate):
        self.spring_rate = spring_rate

    def get_damping_ratio_compression(self):
        return self.damping_ratio_compression

    def set_damping_ratio_compression(self, damping_ratio_compression):
        self.damping_ratio_compression = damping_ratio_compression

    def get_rounding(self):
        return self.rounding

    def set_rounding(self, rounding):
        self.rounding = rounding