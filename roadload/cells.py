class Cells:

    def __init__(self, series_cells):
        self.series_cells = series_cells
        self.rule_compliant = True

    def get_series_cells(self):
        return self.series_cells

    def set_series_cells(self, series_cells):
        self.series_cells = series_cells

    def get_bg_color(self):
        if self.rule_compliant:
            return "#00FF00"
        else:
            return "#FF0000"

    def get_rules_compliance(self):
        return self.rule_compliant