from numpy import pi
from math import sqrt

def calc_sprung_mass_natural_frequency(sprung_mass, spring_rate, rounding):
    return round(0.5 * (1.0/pi) * sqrt(spring_rate/sprung_mass), rounding)

def calc_sprung_mass_damped_frequency(sprung_mass, spring_rate, damping_ratio_compression, rounding):
    f_n = calc_sprung_mass_natural_frequency(sprung_mass, spring_rate, 10)
    return round(f_n*sqrt(1-(damping_ratio_compression**2)), 3)

def calc_unsprung_mass_natural_frequency(wheel_rate, spring_rate, unsprung_mass, rounding)
	return round(1/(2*pi)*sqrt(wheel_rate+spring_rate/unsprung_mass), rounding)

def calc_unsprung_mass_damped_frequency(sprung_mass, spring_rate, damping_ratio_compression, rounding):
    f_n = calc_unsprung_mass_natural_frequency(unsprung_mass, spring_rate, 10)
    return round(f_n*sqrt(1-(damping_ratio_compression**2)), 3)

def calc_eigen_values_vectors_quarter_car()
    return
