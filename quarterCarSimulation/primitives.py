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

        Resources (APA Referenced):
        * Alvarez-Sánchez, E. (2013). A quarter-car suspension system: car body mass estimator and sliding mode control
          [Doctoral dissertation, Faculty of Electrical Mechanical Engineering, Veracruzana College, Zona University].
          Core. https://core.ac.uk/download/pdf/82554529.pdf

        * Jugulkar, L. M., Singh, S. & Sawant, S. M. (2016). Analysis of suspension with variable stiffness and variable
          damping force for automotive applications. Advances in Mechanical Engineering 2016, Volume 8, Issue 5, pages 1–4.
          https://journals.sagepub.com/doi/pdf/10.1177/1687814016648638

        * Kasprzak, J. (2015). Understanding your Dampers: A guide from Jim Kasprzak. Kaz Technologies.
          http://www.kaztechnologies.com/wp-content/uploads/2015/06/A-Guide-To-Your-Dampers-Chapter-from-FSAE-Book-by-Jim-Kasprzak-Updated.pdf

        * Palermo, M. (2009). Effects of a large unsprung mass on the ride comfortof a lightweight fuel-cell urban vehicle
          [Doctoral dissertation, Faculty of Engineering of the University of Pisa]. Core.
          https://core.ac.uk/download/pdf/14697847.pdf

        * Rajeev, N. & Sudi, P. (2019). Natural Frequency, Ride Frequency and their Influence in Suspension System Design.
          Journal of Engineering Research and Application, Volume 9, Issue 3, pages 60-62.
          https://www.ijera.com/papers/vol9no3/Series-3/K0903036064%20.pdf

        * Routely, D. (2017, October 03). Spring Rates & Suspension Frequencies - Plus Calculator! Dr Tuned Racing.
          https://www.drtuned.com/tech-ramblings/2017/10/2/spring-rates-suspension-frequencies        
        
        * Yudianto, A., Kurniadi, N., Adiyasa, I. W. & Arifin, Z. (2019). The Effect of Masses in the Determination of
          Optimal Suspension Damping Coefficient. Journal of Physics: Conference Series, pages 3–4.
          https://iopscience.iop.org/article/10.1088/1742-6596/1273/1/012073/pdf
        """


        return round(0.5 * (1.0/pi) * sqrt(self.spring_rate / self.sprung_mass), self.rounding)

    def get_sprung_mass_damped_frequency(self):
        """Returns an integer
        
        Calculate Sprung Mass Damped Frequency from Natural Frequency

        Resources:
        https://en.wikipedia.org/wiki/Vibration#Free_vibration_with_damping

        Wikipedia is not a 'good' reference, possibly related by reference listed on Wikipedia:
        Simionescu, P.A. (2014). Computer Aided Graphing and Simulation Tools for AutoCAD Users (1st ed.). Boca Raton, FL: CRC Press.
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