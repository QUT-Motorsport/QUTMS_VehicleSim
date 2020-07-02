class Constants:

    def __init__(self, g=0, m=0, P=0, p=0, A=0, Cd=0, mu=0, Cl=0, item=[]):

        if item != []:
            # If object passed as parameter, construct attributes
            self.g = 9.81
            self.m = item.mass
            self.P = item.power
            self.p = item.air_density
            self.A = item.reference_area
            self.Cd = item.coefficient_of_drag
            self.mu = item.coefficient_of_friction
            self.Cl = item.coefficient_of_lift
        else:
            # If parameters are manually inputted
            self.g = g
            self.m = m
            self.P = P
            self.p = p
            self.A = A
            self.Cd = Cd
            self.mu = mu
            self.Cl = Cl

    def get_g(self):
        return self.g

    def set_g(self, g):
        self.g = g

    def get_gravity(self):
        return self.get_g()

    def set_gravity(self, gravity):
        self.set_g(gravity)

    def get_m(self):
        return self.m

    def set_m(self, m):
        self.m = m

    def get_mass(self):
        return self.get_m()

    def set_mass(self, mass):
        self.set_m(mass)

    def get_P(self):
        return self.P

    def set_P(self, P):
        self.P = P

    def get_power(self):
        return self.get_P()

    def set_power(self, power):
        self.set_P(power)

    def get_p(self):
        return self.p

    def set_p(self, p):
        self.p = p

    def get_air_density(self):
        return self.get_p()

    def set_air_density(self, air_density):
        self.set_p(air_density)

    def get_A(self):
        return self.A

    def set_A(self, A):
        self.A = A

    def get_reference_area(self):
        return self.get_A()

    def set_reference_area(self, reference_area):
        self.set_A(reference_area)

    def get_Cd(self):
        return self.Cd

    def set_Cd(self, Cd):
        self.Cd = Cd

    def get_coefficient_of_drag(self):
        return self.get_Cd()

    def set_coefficient_of_drag(self, coefficient_of_drag):
        self.set_Cd(coefficient_of_drag)

    def get_mu(self):
        return self.mu

    def set_mu(self, mu):
        self.mu = mu

    def get_coefficient_of_friction(self):
        return self.get_mu()

    def set_coefficient_of_friction(self, coefficient_of_friction):
        self.set_mu(coefficient_of_friction)

    def get_Cl(self):
        return self.Cl

    def set_Cl(self, Cl):
        self.Cl = Cl

    def get_coefficient_of_lift(self):
        return self.get_Cl()

    def set_coefficient_of_lift(self, coefficient_of_lift):
        self.set_Cl(coefficient_of_lift)