from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField,FloatField, PasswordField, IntegerField, validators, FileField, BooleanField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class dataForm(FlaskForm):
    
    name = StringField("Name", validators=[InputRequired()])
    mat = FileField('Mat File Only', validators=[FileRequired(),FileAllowed({ 'mat', 'MAT'}, 'Mat only!')])
    curvature = StringField("Curvature",validators=[InputRequired()])
    mass = FloatField("Mass",validators=[InputRequired()])
    power = FloatField("Power", validators=[InputRequired()])
    air_density = FloatField("Air Density",validators=[InputRequired()])
    reference_area = FloatField("Reference area",validators=[InputRequired()])
    coefficient_of_drag = FloatField("coefficient of drag",validators=[InputRequired()])
    coefficient_of_friction = FloatField("coefficient of friction",validators=[InputRequired()])
    coefficient_of_lift = FloatField("coefficient of lift", validators=[InputRequired()])
    submit = SubmitField("Submit")

class quarterCarForm(FlaskForm):
    
    name = StringField("Name", validators=[InputRequired()])
    sprungmass = FloatField("Sprung Mass",validators=[InputRequired()])
    unsprungmass = FloatField("Unsprung Mass",validators=[InputRequired()])
    linearspring = FloatField("Linear Spring",validators=[InputRequired()])
    nonlinearspring = FloatField("Non-linear Spring",validators=[InputRequired()])
    damperscompression = FloatField("Linear/Non-Linear in Compression",validators=[InputRequired()])
    dampersrebound = FloatField("Linear/Non-Linear Rebound",validators=[InputRequired()])
    tireslinear = FloatField("Linear Stiffness",validators=[InputRequired()])
    tiresnonlinear = FloatField("Non-Linear Stiffness",validators=[InputRequired()])
    tireslift = FloatField("Saturated During Lift",validators=[InputRequired()])
    bumplinear = FloatField("Bump Linear",validators=[InputRequired()])
    bumpnonlinear = FloatField("Bump Non-Linear",validators=[InputRequired()])
    bumphysteresis = FloatField("Non-Linear with Hysteresis",validators=[InputRequired()])
    submit = SubmitField("Submit")

class accumulatorForm(FlaskForm):
    
    name = StringField("Name", validators=[InputRequired()])
    FoS = FloatField("FoS",validators=[InputRequired()])
    regen = FloatField("Regen",validators=[InputRequired()])
    cellMass = FloatField("Cell Mass",validators=[InputRequired()])
    cellCoverMass = FloatField("Cell Cover Mass",validators=[InputRequired()])
    accumBoxMass = FloatField("Accumulator Mass",validators=[InputRequired()])
    driverMass = FloatField("Driver Mass",validators=[InputRequired()])
    vehicleMass = FloatField("Vehicle Mass",validators=[InputRequired()])
    rollingResistanceCoefficient = FloatField("Rolling Resistance Coefficient",validators=[InputRequired()])
    wheelbase = FloatField("Wheelbase",validators=[InputRequired()])
    gradient = FloatField("Gradient",validators=[InputRequired()])
    frontAxel = FloatField("Front Axel",validators=[InputRequired()])
    rearAxel = FloatField("Rear Axel",validators=[InputRequired()])
    airVelocity = FloatField("Air Velocity",validators=[InputRequired()])
    gearRatio = FloatField("Gear Ratio",validators=[InputRequired()])
    efficiency = FloatField("Efficiency",validators=[InputRequired()])
    wheelRadius = FloatField("Wheel Radius",validators=[InputRequired()])
    nominalVoltage = FloatField("Nominal Voltage",validators=[InputRequired()])
    cellNominalVoltage = FloatField("Cell Nominal Voltage",validators=[InputRequired()])
    cellCapacity = FloatField("Cell Nominal Voltage",validators=[InputRequired()])
    submit = SubmitField("Submit")