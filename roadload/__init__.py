from .accumulator import *
from flask import render_template

class Roadload:
    """Implementation of a Roadload Simulation

    Calculates various accumulator layouts based off a lap simulation
    """

    def __init__(self, constants, min_bricks=6, max_bricks=20, min_cells=8, max_cells=15):

        # Assign parameters to class attributes
        self.constants = constants.__dict__

        # Generate list parameters to iterate through
        self.accumulator = Accumulator(min_bricks, max_bricks, min_cells, max_cells, self.constants)
        self.layouts = self.accumulator.get_brick_layouts()

    def set_simulation_iterations(self, simulation_iterations):
        self.accumulator.set_simulation_iterations(simulation_iterations)
        
    def get_simulation_iterations(self):
        return self.accumulator.get_simulation_iterations()

    def set_roadload_calcs(self):
        self.accumulator.set_roadload_calcs()

    def plot(self):
        return render_template('roadload_graph.html', layouts=self.layouts, accum_spec=self.constants, lap_product=self.get_simulation_iterations(), FoS=self.constants['FoS'])
