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