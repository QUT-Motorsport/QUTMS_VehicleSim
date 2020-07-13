from .layout import Layout
import random

class Accumulator:
    """Implementation of a an Accumulator

    Virtual representation of an Accumulator
    """

    def __init__(self, min_bricks, max_bricks, min_cells, max_cells, constants):

        # Set class attributes
        self.min_bricks = min_bricks
        self.max_bricks = max_bricks
        self.min_cells = min_cells
        self.max_cells = max_cells
        self.constants = constants

        self.brick_iterations = self.iterate_bricks()
        self.brick_configurations = self.get_bricks_configurations()
        self.brick_layouts = self.generate_brick_layouts(constants)

    def base10_round(self, x, base=5):
        return base * round(x/base)

    def generate_brick_layouts(self, inputs):
        driverMass = inputs['driverMass']
        vehicleMass = inputs['vehicleMass']
        accumBoxMass = inputs['accumBoxMass']
        cellCoverMass = inputs['cellCoverMass']
        cellMass = inputs['cellMass']
        Vnom = inputs['nominalVoltage']
        cellMaxVoltage = inputs['cellNominalVoltage']
        cellCapacity = inputs['cellCapacity']

        brick_layouts = []
        for i in self.brick_iterations:
            for y in self.brick_configurations[i]:
                brick_layouts.append(Layout(i, y))
                brick_layouts[len(brick_layouts)-1].generate_cells(self.min_cells, self.max_cells)

                invalid_cell_layouts = []
                for z in brick_layouts[len(brick_layouts)-1].get_cells():
                    z.set_car_mass(driverMass, vehicleMass, accumBoxMass, cellCoverMass, cellMass, i)
                    z.set_accumulator_mass(accumBoxMass, cellCoverMass, cellMass, i)
                    z.set_brick_mass(cellCoverMass, cellMass)
                    z.confirm_rules_compliance(y['Series'], y['Parallel'], Vnom, cellMaxVoltage, cellCapacity, cellMass, cellCoverMass)
                    if not z.get_rules_compliance():
                        invalid_cell_layouts.append(z)

                brick_layouts[len(brick_layouts)-1].set_cells([x for x in brick_layouts[len(brick_layouts)-1].get_cells() if x not in invalid_cell_layouts])
                brick_layouts[len(brick_layouts)-1].set_invalid_cells(invalid_cell_layouts)

        # Remove bricklayouts with 0 possible cell layouts
        for i in range(len(brick_layouts)-1, 0, -1):
            if len(brick_layouts[i].get_cells()) == 0:
                brick_layouts.remove(brick_layouts[i])

        return brick_layouts

    def get_bricks_configurations(self):
        brick_configurations = {}
        for i in self.brick_iterations:
            counter = 2

            layout_possibilities = []
            while counter <= i // 2:
                bricks_in_series = i / counter
                if bricks_in_series % 1 == 0:
                    bricks_in_series = int(bricks_in_series)
                    temp_layout = {}
                    temp_layout['Series'] = bricks_in_series
                    temp_layout['Parallel'] = i//bricks_in_series

                    if layout_possibilities:
                        for y in layout_possibilities:
                            if y['Series'] == temp_layout['Parallel'] and y['Parallel'] == temp_layout['Series']:
                                break
                        else:
                            layout_possibilities.append(temp_layout)
                    else:
                        layout_possibilities.append(temp_layout)
                    
                counter += 1

            brick_configurations[i] = layout_possibilities[:len(layout_possibilities)]

        return brick_configurations


    def iterate_bricks(self):
        test_bricks = list(range(self.min_bricks, self.max_bricks + 1))

        for num, i in enumerate(test_bricks):
            if i > 1:
                for y in range(2, i//2):
                    if (i % y) == 0:
                        break
                else:
                    test_bricks.pop(num)
            else:
                continue

        return test_bricks

    def get_brick_layouts(self):
        return self.brick_layouts

    def set_simulation_iterations(self, simulation_iterations):
        self.simulation_iterations = simulation_iterations
        for num, i in enumerate(self.brick_layouts):
            for y in i.cells:
                car_mass = self.base10_round(y.get_car_mass())
                y.set_lap_simulation(simulation_iterations[car_mass])
        
    def get_simulation_iterations(self):
        return self.simulation_iterations

    def set_roadload_calcs(self):
        for num, i in enumerate(self.brick_layouts):
            for y in i.cells:
                continue