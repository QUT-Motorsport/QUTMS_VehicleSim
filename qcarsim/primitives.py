from numpy import pi
from math import sqrt

class primitives:
    """
    Stores and return values needed for output and calculations of QCar Model
    For values that are not arrays, and require one single instance
    """

    def __init__(self, sprung_mass, spring_rate, damping_ratio_compression, rounding=10):
        self.sprung_mass = sprung_mass
        self.spring_rate = spring_rate
        self.damping_ratio_compression = damping_ratio_compression
        self.rounding = rounding

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
        return round(0.5 * (1.0/pi) * sqrt(self.spring_rate/self.sprung_mass), self.rounding)

    def get_sprung_mass_damped_frequency(self):
        """Returns an integer
        
        Calculate Sprung Mass Damped Frequency from Natural Frequency

        Resources:
        https://en.wikipedia.org/wiki/Vibration#Free_vibration_with_damping
        """
        return round(self.get_sprung_mass_natural_frequency()*sqrt(1-(self.damping_ratio_compression**2)), 3)

    def get_unsprung_mass_natural_frequency(self):
        return 3

    def get_unsprung_mass_damped_frequency(self):
        return 4

    def get_eigen_values(self):
        return 5

    # Attributes

    def get_sprung_mass(self):
        return self.sprung_mass
    
    def set_sprung_mass(self, sprung_mass):
        self.sprung_mass = sprung_mass

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