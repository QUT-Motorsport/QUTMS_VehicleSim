from .cells import Cells
import random

class Layout:
    """Implementation of a an Accumulator Brick Layout

    Virtual representation of a brick
    """

    def __init__(self, num_bricks):

        # Set class attributes
        self.num = num_bricks

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

    def get_bg_color(self):
        return self.bg_hex

    def get_fg_color(self):
        return self.fg_hex

    def set_cells(self, min_cells, max_cells):
        self.cells = []
        for i in list(range(min_cells, max_cells + 1)):
            self.cells.append(Cells(i))

    def get_cells(self):
        return self.cells

    def hex_to_rgb(self, hex):
        hex = hex.lstrip('#')
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))