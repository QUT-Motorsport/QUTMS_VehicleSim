from .layout import Layout
import random

class Accumulator:
    """Implementation of a an Accumulator

    Virtual representation of an Accumulator
    """

    def __init__(self, min_bricks, max_bricks, min_cells, max_cells):

        # Set class attributes
        self.min_bricks = min_bricks
        self.max_bricks = max_bricks
        self.min_cells = min_cells
        self.max_cells = max_cells

        self.brick_layouts = self.iterate_bricks()

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

        brick_layouts = []
        for i in test_bricks:
            brick_layouts.append(Layout(i))
            brick_layouts[len(brick_layouts)-1].set_cells(self.min_cells, self.max_cells)

        return brick_layouts

    def get_brick_layouts(self):
        return self.brick_layouts