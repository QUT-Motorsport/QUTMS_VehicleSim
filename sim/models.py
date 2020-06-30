# sql database sigma   
from . import db
from datetime import datetime

#user sigma
class Lap(db.Model):
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
class QCAR(db.Model):
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

class Accumulator(db.Model):
    __tablename__='accumulator' # good practice to specify table name
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    FoS = db.Column(db.Float)
    regen = db.Column(db.Float)
    cellMass = db.Column(db.Float)
    cellsPack = db.Column(db.Integer)
    packs = db.Column(db.Integer)
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
    def __repr__(self): #string print method
        return "<id: {}, name: {}, FoS: {}, regen: {}, cellMass: {}, cellsPack: {}, packs: {}, accumBoxMass: {}, vehicleMass:{}, driverMass:{}, rollingResistanceCoefficient:{}, wheelbase: {}, gradient: {}, frontAxel: {}, rearAxel: {},bumphysteresis: {},>".format(
                              self.id, self.name, self.FoS, 
                              self.regen, self.cellMass, self.cellsPack, self.packs, self.accumBoxMass, 
                              self.vehicleMass, self.driverMass, self.rollingResistanceCoefficient, 
                              self.wheelbase,self.gradient,self.frontAxel,
                              self.rearAxel,self.airVelocity, self.gearRatio, self.efficiency, self.wheelRadius)