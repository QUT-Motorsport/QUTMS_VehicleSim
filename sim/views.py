from .models import Lap, QCAR
from .forms import dataForm, quarterCarForm
from flask import Blueprint,render_template, redirect, url_for, request, flash, send_file
# from flask_login import LoginManager,login_user,current_user,logout_user, login_required
import datetime
from . import db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys
from vehiclesim import *
import matplotlib.pyplot as plt
window_w = window_h = 0

def check_upload_file(form):
    # get file data from form
    fp = form.mat.data
    filename= fp.filename
    # get the current path of the module file... store file relative to this path
    BASE_PATH= os.path.dirname(__file__)
    
    # uploadfilelocation – directory of this file/static/image
    upload_path= os.path.join(BASE_PATH, 'static/mat', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path= secure_filename(filename)
    # save the file and return the dbupload path
    fp.save(upload_path)
    return db_upload_path

bp = Blueprint('main', __name__)

# Home Page
@bp.route('/')
def live_telemetry():
    dataform = dataForm()
    title = 'QUTMS | Live Telemetry'
    return render_template('live_telemetry.html', title=title, dataform = dataform)

# Upload Lap Page
@bp.route('/upload/lap')
def upload():
    dataform = dataForm()
    title = 'QUTMS | Upload - Lap'
    return render_template('upload.html', title=title, dataform = dataform)

# Analyse table for Plot Mass
@bp.route('/analysis/lap')
def analysis_lap():
    data = Lap.query.order_by(Lap.id.desc()).all()
    title = 'QUTMS | Analysis'
    return render_template('analysis_lap.html', title=title, data=data)

# Analyse table for Quarter Car
@bp.route('/analysis/qcar')
def analysis_qcar():
    data = QCAR.query.order_by(QCAR.id.desc()).all()
    title = 'QUTMS | Analysis'
    return render_template('analysis_qcar.html', title=title, data=data)

# Analyse table for Editing entries in DB
@bp.route('/edit')
def edit():
    data = Lap.query.order_by(Lap.id.desc()).all()
    qcar = QCAR.query.order_by(QCAR.id.desc()).all()
    title = 'QUTMS | Edit'
    return render_template('edit.html', title=title, data=data,qcar=qcar)

# View Help for VD Symbols
@bp.route('/help')
def help():
    title = 'QUTMS | Help'
    return render_template('help.html', title=title)

# Upload parameters for Quarter Car
@bp.route('/upload/qcar-upload')
def qcar_upload():
    dataform = quarterCarForm()
    title = 'QUTMS | QCar'
    return render_template('qcar_upload.html', title=title, dataform=dataform)

# Standard Graph for Plot Mass
@bp.route('/graph/<id>', defaults={'width': None, 'height': None})
@bp.route('/graph/<id>/<width>/<height>')
def graph(id, width=None, height=None):
    if not width or not height:
        return """
        <script>
        (() => window.location.href = window.location.href +
        ['', window.innerWidth, window.innerHeight].join('/'))()
        </script>
        """

    id = Lap.query.filter_by(id=id).first()
    path = os.path.dirname(__file__)

    BASE_PATH= os.path.dirname(__file__)
    
    matfile = os.path.join(BASE_PATH, 'static/mat', id.mat)
    graph_html, fastest_lap, min_speed, max_speed = plotMassLapSim(matfile, id.curvature, int(width), int(height), 9.81, id.mass, id.power, id.air_density, id.reference_area, id.coefficient_of_drag, id.coefficient_of_friction, id.coefficient_of_lift)
    title = 'QUTMS | Graph'
    return render_template('graph.html',min_speed=min_speed,max_speed=max_speed, graph_html=graph_html,title=title, name=id.name, fastest_lap=fastest_lap[2:], id=id)

# GG Only Diagram for Plot Mass
@bp.route('/gg/<id>', defaults={'width': None, 'height': None})
@bp.route('/gg/<id>/<width>/<height>')
def gg_diagram(id, width=None, height=None):
    if not width or not height:
        return """
        <script>
        (() => window.location.href = window.location.href +
        ['', window.innerWidth, window.innerHeight].join('/'))()
        </script>
        """

    id = Lap.query.filter_by(id=id).first()
    path = os.path.dirname(__file__)

    BASE_PATH= os.path.dirname(__file__)
    
    matfile = os.path.join(BASE_PATH, 'static/mat', id.mat)
    graph_html, fastest_lap, min_speed, max_speed = plotMassGG(matfile, id.curvature, int(width), int(height), 9.81, id.mass, id.power, id.air_density, id.reference_area, id.coefficient_of_drag, id.coefficient_of_friction, id.coefficient_of_lift)
    title = 'QUTMS | GG Diagram'
    return render_template('gg_diagram.html',id=id,min_speed=min_speed,max_speed=max_speed, graph_html=graph_html,title=title, name=id.name, fastest_lap=fastest_lap[2:])

# Delete Lap Entry
@bp.route('/lrm/<id>')
def lrm(id):
    info = Lap.query.filter_by(id=id).first()
    path = os.path.dirname(__file__)
    BASE_PATH= os.path.dirname(__file__)
    matfile = os.path.join(BASE_PATH, 'static/mat', info.mat)
    Lap.query.filter_by(id=id).delete()
    db.session.commit()
    os.remove(matfile)
    flash("File removed" )
    return redirect('/edit')

# Delete Quarter Car entry
@bp.route('/qrm/<id>')
def qrm(id):
    info = QCAR.query.filter_by(id=id).first()
    QCAR.query.filter_by(id=id).delete()
    db.session.commit()
    flash("File removed" )
    return redirect('/edit')

# Uploads data object for Plot Mass
@bp.route('/data', methods=['GET','POST'])
def data():
    dataform = dataForm()
    if dataform.validate_on_submit():
        db_file_path=check_upload_file(dataform)
        #insert item into database
        newitem = Lap(id = datetime.datetime.now(),
                    name=dataform.name.data,
                    mat = db_file_path,
                    curvature = dataform.curvature.data,
                    mass = dataform.mass.data,
                    power = dataform.power.data,
                    air_density = dataform.air_density.data,
                    reference_area = dataform.reference_area.data,
                    coefficient_of_drag = dataform.coefficient_of_drag.data,
                    coefficient_of_friction = dataform.coefficient_of_friction.data,
                    coefficient_of_lift = dataform.coefficient_of_lift.data
                    )

        #add the object to the db session
        db.session.add(newitem)

        #commit to the database
        db.session.commit()
        flash('The file was successfully uploaded to the database', 'success')
        print('Added', 'success')
    return redirect(url_for('main.upload'))

# Upload data for Quarter Car
@bp.route('/upload/qcardata', methods=['GET','POST'])
def qcar_data():
    dataform = quarterCarForm()
    if dataform.validate_on_submit():
        newitem = QCAR(id = datetime.datetime.now(),
                    name=dataform.name.data,
                    sprungmass = dataform.sprungmass.data,
                    unsprungmass = dataform.unsprungmass.data,
                    linearspring = dataform.linearspring.data,
                    nonlinearspring = dataform.nonlinearspring.data,
                    damperscompression = dataform.damperscompression.data,
                    dampersrebound = dataform.dampersrebound.data,
                    tireslinear = dataform.tireslinear.data,
                    tiresnonlinear = dataform.tiresnonlinear.data,
                    tireslift = dataform.tireslift.data,
                    bumplinear = dataform.bumplinear.data,
                    bumpnonlinear = dataform.bumpnonlinear.data,
                    bumphysteresis = dataform.bumphysteresis.data
                    )
        #add the object to the db session
        db.session.add(newitem)
        #commit to the database
        db.session.commit()
        flash('The file was successfully uploaded to the database', 'success')
        print('Added', 'success')
    return redirect(url_for('main.qcar_upload'))

#download all graphs
@bp.route('/export_button', methods=['GET', "POST"])
def export_generate_all():
    #load pickled graphs
    fig = pickle.load(open('graph_all.p','rb'))
    #save as svg internally
    fig.savefig('sim/static/svg/graph_all.svg')
    #return svg to client
    return send_file('static/svg/graph_all.svg', as_attachment=True, attachment_filename='graph_output_all.svg')    

#download gg graph
@bp.route('/export_button_gg')
def export_generate_gg():
    #load pickled gg graph
    fig_gg = pickle.load(open('graph_gg.p','rb'))
    #save as svg internally
    fig_gg.savefig('sim/static/svg/graph_gg.svg')
    #return svg to client
    return send_file('static/svg/graph_gg.svg', as_attachment=True, attachment_filename='graph_output_gg.svg')

    