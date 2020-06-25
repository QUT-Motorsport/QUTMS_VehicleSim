from numpy import pi
from math import sqrt

# https://www.ijera.com/papers/vol9no3/Series-3/K0903036064%20.pdf
# https://www.drtuned.com/tech-ramblings/2017/10/2/spring-rates-suspension-frequencies
# https://core.ac.uk/download/pdf/14697847.pdf
# http://www.kaztechnologies.com/wp-content/uploads/2015/06/A-Guide-To-Your-Dampers-Chapter-from-FSAE-Book-by-Jim-Kasprzak-Updated.pdf
# https://core.ac.uk/download/pdf/82554529.pdf
# https://journals.sagepub.com/doi/pdf/10.1177/1687814016648638
# https://iopscience.iop.org/article/10.1088/1742-6596/1273/1/012073/pdf

def calc_sprung_mass_natural_frequency(sprung_mass, spring_rate, rounding):
    return round(0.5 * (1.0/pi) * sqrt(spring_rate/sprung_mass), rounding)

# https://en.wikipedia.org/wiki/Vibration#Free_vibration_with_damping

def calc_sprung_mass_damped_frequency(sprung_mass, spring_rate, damping_ratio_compression, rounding):
    f_n = calc_sprung_mass_natural_frequency(sprung_mass, spring_rate, 10)
    return round(f_n*sqrt(1-(damping_ratio_compression**2)), 3)

def calc_unsprung_mass_natural_frequency():
    return 3

def calc_unsprung_mass_damped_frequency():
    return 4

def calc_eigen_values_and_Vectors_of_quarter_car():
    return 5