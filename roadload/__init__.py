from .accumulator import *
from flask import render_template

class Roadload:
    """Implementation of a Roadload Simulation

    Calculates various accumulator layouts based off a lap simulation
    """

    def __init__(self, constants, simulation_iterations, min_bricks=6, max_bricks=20, min_cells=8, max_cells=15):

        # Assign parameters to class attributes
        self.constants = constants.__dict__
        self.simulation_iterations = simulation_iterations

        # Generate list parameters to iterate through
        accumulator = Accumulator(min_bricks, max_bricks, min_cells, max_cells)
        self.layouts = accumulator.get_brick_layouts()

    def plot(self):
        return render_template('roadload_graph.html', layouts=self.layouts, accum_spec=self.constants, lap_product=self.simulation_iterations, FoS=self.constants['FoS'])
