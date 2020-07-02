from qcarsim import *

def html_tag(inputVariable, tag):
    return "<"+tag+">"+str(inputVariable)+"</"+tag+">"

def load_template(headings, values):
    output = ""
    for i in range(len(headings)):
        output += html_tag(headings[i], "strong")
        output += html_tag(values[i], "p")
    return output