from math import cos

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

    def set_car_mass(self, driverMass, vehicleMass, accumBoxMass, cellCoverMass, cellMass, bricks):
        self.car_mass = round(driverMass + vehicleMass + accumBoxMass + (cellCoverMass / 1000 * self.get_cells_total() * bricks) + (cellMass / 1000 * self.get_cells_total() * bricks), 3)

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

    def set_rear_rolling_resistance(self, tire_friction_coefficient, base_weight, gravity, slope, rearAxle, wheelBase):
        self.rear_rolling_resistance = tire_friction_coefficient * base_weight * gravity * cos(slope) * (rearAxle / wheelBase)

    def get_rear_rolling_resistance(self):
        return self.rear_rolling_resistance

    def set_front_rolling_resistance(self, tire_friction_coefficient, base_weight, gravity, slope, frontAxle, wheelBase):
        self.front_rolling_resistance = tire_friction_coefficient * base_weight * gravity * cos(slope) * (frontAxle / wheelBase)

    def get_front_rolling_resistance(self):
        return self.front_rolling_resistance