from .primitives import *

class QuarterCarSimulation:
    """Implementation of a Quarter Car Model

    Calculates the kinematics and dynamics of a suspension via inputs
    """

    def __init__(self, sprung_mass, unsprung_mass, wheel_rate, spring_rate, damping_ratio_compression):

        # Assign class parameters to constants class
        self.primitives = Primitives(sprung_mass, unsprung_mass, wheel_rate, spring_rate, damping_ratio_compression)

        # Format all values into one dictionary
        self.values = {}
        self.values['primitives'] = self.primitives.get_values()

        # Format headings to dictionary
        self.headings = {}
        self.headings['primitives'] = self.primitives.get_headings()

    def html_tag(self, inputVariable, tag):
        return "<"+tag+">"+str(inputVariable)+"</"+tag+">"

    def load_template(self, values, headings=[]):

        # If no headings are passed, values is a string with the dict key to open to display
        if (headings == []):
            headings = self.headings[values]
            values = self.values[values]

        output = ""
        for i in range(len(headings)):
            output += self.html_tag(headings[i], "strong")
            output += self.html_tag(values[i], "p")
        return output

    def get_values(self):
        return self.values
        