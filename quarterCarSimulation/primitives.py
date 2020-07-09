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

        Resources (APA Referenced, Not all used for final calculation):
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
        """
        Plan: Return a list with all of the eigen values contained within.

        Resources:
        Google Search: "eigenvalues an eigenvectors of natural frequency"
        https://lpsa.swarthmore.edu/MtrxVibe/EigApp/EigVib.html
        http://www2.me.rochester.edu/courses/ME443/NASTRAN/Chpt3RealEigenvalueAnalysis.pdf
        https://encyclopediaofmath.org/wiki/Natural_frequencies
        https://www.researchgate.net/post/Why_the_calculation_of_natural_frequencyeigenvalue_by_FEMfinite_element_method_do_not_converged_while_the_elements_growth
        https://www.researchgate.net/post/How_can_we_find_the_eigenvectors_and_eigenvalues_when_have_unknow_values_in_damping_matrix
        https://pdfs.semanticscholar.org/aee7/3d8ed1833deeaf83db335f067878448bd43f.pdf

        Google Search: "eigenvalues an eigenvectors of qcar natural frequency"
        https://www.mathworks.com/matlabcentral/answers/334812-eigenvalues-and-eigenvectors-how-do-i-work-out-which-eigenvalue-corresponds-to-which-eigenvector
        https://www.researchgate.net/publication/322020905_PARAMETRIC_ANALYSIS_OF_A_QUARTER_CAR_VEHICLE_MODEL
        https://engineering.purdue.edu/~deadams/ME563/HW5_10_solns.pdf
        https://books.google.com.au/books?id=36kg2DJiy7cC&pg=PA195&lpg=PA195&dq=eigenvalues+and+eigenvectors+of+a+car+natural+frequency&source=bl&ots=JYgFDBI4gn&sig=ACfU3U30ZAWNtexfqMxLSwAV_DKWvZC1gA&hl=en&sa=X&ved=2ahUKEwiexPfMhr_qAhV6wzgGHemGAVs4ChDoATACegQIBxAB#v=onepage&q=eigenvalues%20and%20eigenvectors%20of%20a%20car%20natural%20frequency&f=false
        https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2017/ENU/NINCAD-SelfTraining/files/GUID-978425AB-D2FA-491B-8D39-BD1A757F3BBD-htm.html
        https://docs.plm.automation.siemens.com/data_services/resources/nxnastran/12/help/tdoc/en_US/pdf/basic_dynamics.pdf

        Google Search: "natural frequency from eigenvalues"
        https://ocw.mit.edu/courses/mechanical-engineematlabring/2-004-systems-modeling-and-control-ii-fall-2007/assignments/sol09.pdf

        Google Search: "natural frequency from eigenvalues qcar"
        http://downloads.hindawi.com/archive/2012/863061.pdf
        https://ep.liu.se/ecp/076/071/ecp12076071.pdf

        Google Search: "stiffness matrix qcar"
        http://people.duke.edu/~hpgavin/cee421/matrix.pdf
        https://www.researchgate.net/post/What_are_the_typical_stiffness_values_while_designing_car_chassis

        Google Search: "mass matrix qcar"
        https://en.wikipedia.org/wiki/Mass_matrix
        http://kis.tu.kielce.pl/mo/COLORADO_FEM/colorado/IFEM.Ch31.pdf
        http://faculty.washington.edu/averess/ME478/dynamics.pdf
        http://people.duke.edu/~hpgavin/cee541/StructuralElements.pdf

        need to do more research on stiffness matrix and mass matrix
        """
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