from .cells import Cells
import random

class Layout:
    """Implementation of a an Accumulator Brick Layout

    Virtual representation of a brick
    """

    def __init__(self, num_bricks, configuration):

        # Set class attributes
        self.num = num_bricks
        self.configuration = configuration

        # Set background colour
        r = lambda: random.randint(0,255)
        self.bg_hex = '#%02X%02X%02X' % (r(),r(),r())

        # Set fg colour
        rgb_bg = self.hex_to_rgb(self.bg_hex)
        luminance = (0.299*rgb_bg[0] + 0.587*rgb_bg[1] + 0.114*rgb_bg[2])
        self.fg_hex = "#FFFFFF" if luminance < 120 else "#000000"

    def get_bricks(self):
        return self.num

    def set_bricks(self, num):
        self.num = num

    def get_bricks_series(self):
        return self.configuration['Series']

    def get_bricks_parallel(self):
        return self.configuration['Parallel']

    def get_bg_color(self):
        return self.bg_hex

    def get_fg_color(self):
        return self.fg_hex

    def set_cells(self, cells):
        self.cells = cells

    def generate_cells(self, min_cells, max_cells):
        self.cells = []
        for i in list(range(min_cells, max_cells + 1)):
            for y in list(range(1, max_cells + 1)):
                self.cells.append(Cells(i, y))

    def get_cells(self):
        return self.cells

    def set_invalid_cells(self, invalid_cells):
        self.invalid_cells = invalid_cells

    def get_invalid_cells(self):
        return self.invalid_cells

    def hex_to_rgb(self, hex):
        hex = hex.lstrip('#')
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))