from math import cos
from numpy import dot

class Cells:

    def __init__(self, cells_series, cells_parallel):
        self.cells_series = cells_series
        self.cells_parallel = cells_parallel
        self.rule_issue = ''

    def get_cells_series(self):
        return self.cells_series

    def set_cells_series(self, cells_series):
        self.cells_series = cells_series

    def get_cells_parallel(self):
        return self.cells_parallel

    def set_cells_parallel(self, cells_parallel):
        self.cells_parallel = cells_parallel

    def get_cells_total(self):
        return self.cells_parallel * self.cells_series

    def get_bg_color(self):
        if not self.rule_issue:
            return "#00FF00"
        else:
            return "#FF0000"
    
    def confirm_rules_compliance(self, bricks_series, bricks_parallel, Vnom, cellMaxVoltage, cellCapacity, cellMass, cellCoverMass):
        
        # Check if cells exceed maximum nominal voltage
        if self.cells_series * bricks_series * cellMaxVoltage > Vnom:
            self.rule_issue = 'Exceeds Maximum Nominal Voltage of ' + str(Vnom) + 'V by ' + str(int(self.cells_series * bricks_series * cellMaxVoltage - Vnom)) + 'V'
        if self.cells_parallel * bricks_parallel * cellMaxVoltage > Vnom:
            self.rule_issue = 'Exceeds Maximum Nominal Voltage of ' + str(Vnom) + 'V by ' + str(int(self.cells_parallel * bricks_parallel * cellMaxVoltage - Vnom)) + 'V'

        # Check if brick exceeds maximum 6 MJ per brick
        if self.cells_series * self.cells_parallel * (cellCapacity * 1000) * cellMaxVoltage * 3.6 > 6000000:
            self.rule_issue = 'Exceeds maximum capacity per brick of 6MJ'

        # Check if brick exceeds maximum 12 KG per brick
        if self.cells_series * self.cells_parallel * (cellMass + cellCoverMass) > 12000:
            self.rule_issue = 'Exceeds maximum brick weight of 12KG'

    def get_rules_compliance(self):
        return not bool(self.rule_issue)

    def get_rule_issue(self):
        return self.rule_issue

    def get_car_mass(self):
        return self.car_mass

    def get_base_weight(self):
        return self.base_weight

    def set_car_mass(self, driverMass, vehicleMass, accumBoxMass, cellCoverMass, cellMass, bricks):
        self.car_mass = round(driverMass + vehicleMass + accumBoxMass + (cellCoverMass / 1000 * self.get_cells_total() * bricks) + (cellMass / 1000 * self.get_cells_total() * bricks), 3)
        self.base_weight = self.car_mass - driverMass

    def set_lap_simulation(self, lap_simulation):
        self.lap_simulation = lap_simulation

    def get_lap_simulation(self):
        return self.lap_simulation

    def set_accumulator_mass(self, accumBoxMass, cellCoverMass, cellMass, bricks):
        self.accumulator_mass = round(accumBoxMass + (cellCoverMass / 1000 * self.get_cells_total() * bricks) + (cellMass / 1000 * self.get_cells_total() * bricks), 3)

    def get_accumulator_mass(self):
        return self.accumulator_mass

    def set_brick_mass(self, cellCoverMass, cellMass):
        self.brick_mass = round((cellCoverMass / 1000 * self.get_cells_total()) + (cellMass / 1000 * self.get_cells_total()), 3)

    def get_brick_mass(self):
        return self.brick_mass

    def set_rear_rolling_resistance(self, tire_friction_coefficient, gravity, slope, rearAxle, wheelBase):
        self.rear_rolling_resistance = round(tire_friction_coefficient * self.base_weight * gravity * cos(slope) * (rearAxle / wheelBase), 4)

    def get_rear_rolling_resistance(self):
        return self.rear_rolling_resistance

    def set_front_rolling_resistance(self, tire_friction_coefficient, gravity, slope, frontAxle, wheelBase):
        self.front_rolling_resistance = round(tire_friction_coefficient * self.base_weight * gravity * cos(slope) * (frontAxle / wheelBase), 4)

    def get_front_rolling_resistance(self):
        return self.front_rolling_resistance

    def list_subtract(self, input_list, value):
        return [x - value for x in input_list]

    def set_aero_force(self, wind_velocity, air_density=0, coefficient_of_drag=0, frontal_area=0, velocity=[]):
        if air_density == 0 and coefficient_of_drag == 0 and frontal_area == 0 and velocity == []:
            velocity = self.lap_simulation.get_velocity()
            air_density = self.lap_simulation.get_vehicle_constants().get_air_density()
            coefficient_of_drag = self.lap_simulation.get_vehicle_constants().get_coefficient_of_drag()
            frontal_area = self.lap_simulation.get_vehicle_constants().get_reference_area()

        actual_velocity = [(x - wind_velocity)**2 for x in velocity]
        self.aero_force = [0.5 * air_density * coefficient_of_drag * frontal_area * x for x in actual_velocity]

    def get_aero_force(self):
        return self.aero_force

    def set_tractive_force(self):
        self.tractive_force = []
        accel = self.get_lap_simulation().get_a_long()

        if len(accel) == len(self.aero_force):
            for i in range(len(self.aero_force)):
                self.tractive_force.append((self.car_mass * accel[i]) + self.aero_force[i] + self.front_rolling_resistance + self.rear_rolling_resistance)
        print(self.tractive_force[:4])
        

    def get_tractive_force(self):
        return self.tractive_force