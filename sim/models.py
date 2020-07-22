# sql database sigma   
from . import db
from datetime import datetime
from flask_login import UserMixin

#user sigma
class User(db.Model, UserMixin):
    __tablename__='user' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    def __repr__(self): #string print method
        return "<email: {}, id: {}>".format(
            self.email, self.id)

class Lap(db.Model, UserMixin):
    __tablename__='lap' # good practice to specify table name
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    mat = db.Column(db.String(255))
    curvature = db.Column(db.String(50))
    mass = db.Column(db.Float)
    power = db.Column(db.Float)
    air_density = db.Column(db.Float)
    reference_area = db.Column(db.Float)
    coefficient_of_drag = db.Column(db.Float)
    coefficient_of_friction = db.Column(db.Float)
    coefficient_of_lift = db.Column(db.Float)
    def __repr__(self): #string print method
        return "<id: {}, name: {}, mat: {}, curvature: {}, mass: {}, power:{}, air_density:{}, reference_area:{}, coefficient_of_drag: {}, coefficient_of_friction: {},coefficient_of_lift: {}>".format(
                              self.id, self.name, self.mat, 
                              self.curvature, self.mass, 
                              self.power, self.air_density, self.reference_area, 
                              self.coefficient_of_drag,self.coefficient_of_friction,self.coefficient_of_lift,)
class QCAR(db.Model, UserMixin):
    __tablename__='qcar' # good practice to specify table name
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    sprungmass = db.Column(db.Float)
    unsprungmass = db.Column(db.Float)
    linearspring = db.Column(db.Float)
    nonlinearspring = db.Column(db.Float)
    damperscompression = db.Column(db.Float)
    dampersrebound = db.Column(db.Float)
    tireslinear = db.Column(db.Float)
    tiresnonlinear = db.Column(db.Float)
    tireslift = db.Column(db.Float)
    bumplinear = db.Column(db.Float)
    bumpnonlinear = db.Column(db.Float)
    bumphysteresis = db.Column(db.Float)
    def __repr__(self): #string print method
        return "<id: {}, name: {}, sprungmass: {}, unsprungmass: {}, linearspring: {}, nonlinearspring: {}, damperscompression:{}, dampersrebound:{}, tireslinear:{},tiresnonlinear: {}, tireslift: {},bumplinear: {},bumpnonlinear: {},bumphysteresis: {},>".format(
                              self.id, self.name, self.sprungmass, 
                              self.unsprungmass, self.linearspring, self.nonlinearspring, 
                              self.damperscompression, self.dampersrebound, self.tireslinear, 
                              self.tiresnonlinear,self.tireslift,self.bumplinear,
                              self.bumpnonlinear,self.bumphysteresis)

class Accumulator(db.Model, UserMixin):
    __tablename__='accumulator' # good practice to specify table name
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    FoS = db.Column(db.Float)
    regen = db.Column(db.Float)
    cellMass = db.Column(db.Float)
    cellCoverMass = db.Column(db.Float)
    accumBoxMass = db.Column(db.Float)
    vehicleMass = db.Column(db.Float) # Excludes Driver, Accumulator Box/Hardware and Cells
    driverMass = db.Column(db.Float)
    rollingResistanceCoefficient = db.Column(db.Float)
    wheelbase = db.Column(db.Float)
    gradient = db.Column(db.Float)
    frontAxel = db.Column(db.Float) # longitudinal distance between front axel to the centre of gravity (Any input is multiplied by L)
    rearAxel = db.Column(db.Float) # longitudinal distance between rear axel to the centre of gravity (Any input is multiplied by L)
    airVelocity = db.Column(db.Float) # Wind
    gearRatio = db.Column(db.Float)
    efficiency = db.Column(db.Float)
    wheelRadius = db.Column(db.Float)
    nominalVoltage = db.Column(db.Float)
    cellNominalVoltage = db.Column(db.Float)
    cellCapacity = db.Column(db.Float)
    def __repr__(self): #string print method
        return "<id: {}, name: {}, FoS: {}, regen: {}, cellMass: {}, cellCoverMass: {}, accumBoxMass: {}, vehicleMass:{}, driverMass:{}, rollingResistanceCoefficient:{}, wheelbase: {}, gradient: {}, frontAxel: {}, rearAxel: {}, airVelocity: {}, gearRatio: {}, efficiency: {}, wheelRadius: {}>".format(
                              self.id, self.name, self.FoS, 
                              self.regen, self.cellMass, self.cellCoverMass, self.accumBoxMass, 
                              self.vehicleMass, self.driverMass, self.rollingResistanceCoefficient, 
                              self.wheelbase,self.gradient,self.frontAxel,
                              self.rearAxel,self.airVelocity, self.gearRatio, self.efficiency, self.wheelRadius)