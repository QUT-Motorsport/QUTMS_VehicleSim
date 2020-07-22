from .models import Lap, QCAR, Accumulator
from .forms import dataForm, quarterCarForm, accumulatorForm
from flask import Blueprint,render_template, redirect, url_for, request, flash, send_file
from flask_login import LoginManager,login_user,current_user,logout_user, login_required
import datetime
from . import db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys
from plotmass import PlotMassSimulation
from roadload import Roadload
from pypresence import Presence
from github import Github
from dotenv import load_dotenv, find_dotenv
from scipy.io import savemat
# globals
window_w = window_h = 0
mat_upload_number = 0

# discord rich presence
rpc_activated = False
try:
    client_id = '708329075546128437'
    RPC = Presence(client_id)
    RPC.connect()
    rpc_activated = True
except:
    rpc_activated = False

# github
load_dotenv(find_dotenv())
g = Github(os.getenv("GITHUB"))

# Initalise blueprint
bp = Blueprint('main', __name__)

# Helper functions



def check_upload_file(form):
    global mat_upload_number
    # get file data from form
    fp = form.mat.data
    # get the current path of the module file... store file relative to this path
    BASE_PATH= os.path.dirname(__file__)
    
    mat_upload_number += 1
    mat_file_name = 'track_' + str(mat_upload_number) + '.mat'
    # uploadfilelocation – directory of this file/static/image
    upload_path= os.path.join(BASE_PATH, 'static/mat', secure_filename(mat_file_name))
    # store relative path in DB as image location in HTML is relative
    db_upload_path= secure_filename(mat_file_name)
    # save the file and return the dbupload path
    fp.save(upload_path)
    return db_upload_path

def fetch_mat_file(mat_name):
    BASE_PATH = os.path.dirname(__file__)
    matfile = os.path.join(BASE_PATH, 'static/mat', mat_name)
    return matfile

def base10_round(x, base=5):
    return base * round(x/base)

# Generate values from 150% car weight to 50% car weight
def stepped_values(max_value, step=5):
    values = []
    i = base10_round(max_value * 1.5, step)
    while i > max_value / 2:
        values.append(i)
        i -= step
    return values

# Home page
@bp.route('/')
def home():
    if rpc_activated:
        RPC.update(state="Our History", details="Browsing", large_image="qut-logo")

    try:
        repo = g.get_repo("QUT-Motorsport/QUTMS_VehicleSim")
        open_issues = repo.get_issues(state='open')
        labels = repo.get_topics()
        commits = repo.get_commits()
        latest_commits = []
        for commit in commits[:6]:
            latest_commit = {}
            latest_commit["title"] = commit.commit.message
            latest_commit["url"] = commit.commit.html_url
            latest_commit["author"] = commit.commit.author.name
            latest_commit["date"] = commit.commit.author.date
            latest_commits.append(latest_commit)
        return render_template('home.html', issues=open_issues, labels=labels, commits=latest_commits)
    except:
        print("Github API Call was unsuccessful")       
        return render_template('home.html')

# Telemetry Page
@bp.route('/telemetry')
def live_telemetry():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    dataform = dataForm()
    title = 'QUTMS | Live Telemetry'
    if rpc_activated:
        RPC.update(state="Telemetry", details="Analyzing...", large_image="qut-logo")
    return render_template('live_telemetry.html', title=title, dataform = dataform)

# Upload Lap Page
@bp.route('/upload/lap')
def upload():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    dataform = dataForm()
    title = 'QUTMS | Upload - Lap'
    if rpc_activated:
        RPC.update(state="Simulation", details="Uploading Lap Time", large_image="qut-logo")
    return render_template('upload.html', title=title, dataform = dataform)

# Analyse table for Plot Mass
@bp.route('/analysis/lap')
def analysis_lap():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')    
    data = Lap.query.order_by(Lap.id.desc()).all()
    title = 'QUTMS | Analysis'
    if rpc_activated:
        RPC.update(state="Point Mass Lap Simulations", details="Analyzing...", large_image="qut-logo")
    return render_template('analysis_lap.html', title=title, data=data)

# Analyse table for Quarter Car
@bp.route('/analysis/qcar')
def analysis_qcar():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    data = QCAR.query.order_by(QCAR.id.desc()).all()
    title = 'QUTMS | Analysis'
    if rpc_activated:
        RPC.update(state="Quarter Car", details="Analyzing...", large_image="qut-logo")
    return render_template('analysis_qcar.html', title=title, data=data)

# Standard Output for QCAR Model
@bp.route('/qcar/<id>', defaults={'width': None, 'height': None})
@bp.route('/qcar/<id>/<width>/<height>')
def qcar(id, width=None, height=None):

    # Fetch Browser Height and Width
    if not width or not height:
        return """
        <script>
        (() => window.location.href = window.location.href +
        ['', window.innerWidth, window.innerHeight].join('/'))()
        </script>
        """

    # Fetch QCAR instance by ID
    id = QCAR.query.filter_by(id=id).first()
    qcar_m_s = id.sprungmass            # Sprung Mass           (kg)
    qcar_m_u = id.unsprungmass          # Unsprung Mass         (kg)
    qcar_s_l = id.linearspring          # Linear Spring Rate?   (N/m)
    qcar_s_nl = id.nonlinearspring      # Non-Linear Spring?    (?)
    qcar_d_c = id.damperscompression    # Dampering Ratio Comp? (ratio)
    qcar_d_r = id.dampersrebound        # Dampers Rebound?      (?)
    qcar_t_l = id.tireslinear           # Tires Linear?         (?)
    qcar_t_nl = id.tiresnonlinear       # Tires Non-Linear?     (?)
    qcar_t_L = id.tireslift             # Tires Lift?           (?)
    qcar_b_l = id.bumplinear            # Bump Linear?          (?)
    qcar_b_nl = id.bumpnonlinear        # Bump Non-Linear?      (?)
    qcar_b_h = id.bumphysteresis        # Bump Hysteresis?      (?)

    qcar_primitive = primitives(qcar_m_s, qcar_s_l, qcar_d_c)

    headings = ["Sprung Mass Natural Frequency (Hz)",
                "Sprung Mass Damped Frequency (Hz)",
                "Unsprung Mass Natural Frequency",
                "Unsprung Mass Damped Frequency",
                "Eigen Values and Eigen Vectors of the Quarter Car"]

    values = [qcar_primitive.get_sprung_mass_natural_frequency(),
              qcar_primitive.get_sprung_mass_damped_frequency(),
              qcar_primitive.get_unsprung_mass_natural_frequency(),
              qcar_primitive.get_unsprung_mass_damped_frequency(),
              qcar_primitive.get_eigen_values()]


    data = load_template(headings, values)

    title = 'QUTMS | QCAR'
    return render_template('qcar_output.html',title=title,id=id,name=id.name,output_html=data)


# Analyse table for Editing entries in DB
@bp.route('/edit')
def edit():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    data = Lap.query.order_by(Lap.id.desc()).all()
    qcar = QCAR.query.order_by(QCAR.id.desc()).all()
    title = 'QUTMS | Edit'
    if rpc_activated:
        RPC.update(state="Vehicle Simulations", details="Editing", large_image="qut-logo")
    return render_template('edit.html', title=title, data=data,qcar=qcar)

# View Help for VD Symbols
@bp.route('/help')
def help():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    title = 'QUTMS | Help'
    if rpc_activated:
        RPC.update(state="Vehicle Dynamics", details="Studying", large_image="qut-logo")
    return render_template('help.html', title=title)

# Upload parameters for Quarter Car
@bp.route('/upload/qcar-upload')
def qcar_upload():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    dataform = quarterCarForm()
    title = 'QUTMS | QCar'
    if rpc_activated:
        RPC.update(state="Quarter Car", details="Uploading", large_image="qut-logo")
    return render_template('qcar_upload.html', title=title, dataform=dataform)

# Standard Graph for Plot Mass
@bp.route('/graph/<id>', defaults={'width': None, 'height': None})
@bp.route('/graph/<id>/<width>/<height>')
def graph(id, width=None, height=None):
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    if not width or not height:
        return """
        <script>
        (() => window.location.href = window.location.href +
        ['', window.innerWidth, window.innerHeight].join('/'))()
        </script>
        """

    # Set tab title
    title = 'QUTMS | Graph'

    # Fetch lap instance from DB
    id = Lap.query.filter_by(id=id).first()

    # Fetch mat file for simulation input
    matfile = fetch_mat_file(id.mat)

    # Initialise Simulation
    simulation = PlotMassSimulation(matfile, id.curvature, int(width), int(height), id.mass, id.power, id.air_density, id.reference_area, id.coefficient_of_drag, id.coefficient_of_friction, id.coefficient_of_lift)

    # Pickle graph & stats for download
    simulation.pickle(simulation.plot(), "graph_all.p")

    # Update discord rich presence
    if rpc_activated:
        RPC.update(state= str(int(id.mass)) + 'kg @ ' + str(int(id.power)) + 'W - ' + str(simulation.get_fastest_lap()), details=str(id.name) + ' - View Plots', large_image="qut-logo")

    return render_template('graph.html', graph_html=simulation.plot_html(), title=title, name=id.name, fastest_lap=simulation.get_fastest_lap()[2:], id=id)

# GG Only Diagram for Plot Mass
@bp.route('/gg/<id>', defaults={'width': None, 'height': None})
@bp.route('/gg/<id>/<width>/<height>')
def gg_diagram(id, width=None, height=None):
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    if not width or not height:
        return """
        <script>
        (() => window.location.href = window.location.href +
        ['', window.innerWidth, window.innerHeight].join('/'))()
        </script>
        """

    # Set tab title
    title = 'QUTMS | GG Diagram'

    # Fetch lap instance from DB
    id = Lap.query.filter_by(id=id).first()

    # Fetch mat file for simulation input
    matfile = fetch_mat_file(id.mat)

    # Initialise Simulation
    simulation = PlotMassSimulation(matfile, id.curvature, int(width), int(height), id.mass, id.power, id.air_density, id.reference_area, id.coefficient_of_drag, id.coefficient_of_friction, id.coefficient_of_lift)
    
    # Pickle graph & stats for download
    simulation.pickle(simulation.plot_gg(), "graph_gg.p")

    # Update discord rich presence
    if rpc_activated:
        RPC.update(state= str(int(id.mass)) + 'kg @ ' + str(int(id.power)) + 'W - ' + str(simulation.get_fastest_lap()), details=str(id.name), large_image="qut-logo")

    return render_template('gg_diagram.html', id=id, graph_html=simulation.plot_gg_html(), title=title, name=id.name, fastest_lap=simulation.get_fastest_lap()[2:])

# Standard Graph for Speed v Curvature
@bp.route('/speedcurvature/<id>', defaults={'width': None, 'height': None})
@bp.route('/speedcurvature/<id>/<width>/<height>')
def speedcurvature(id, width=None, height=None):
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    if not width or not height:
        return """
        <script>
        (() => window.location.href = window.location.href +
        ['', window.innerWidth, window.innerHeight].join('/'))()
        </script>
        """

    # Set tab title
    title = 'QUTMS | Speed v Curvature'

    # Fetch lap instance from DB
    id = Lap.query.filter_by(id=id).first()

    # Fetch mat file for simulation input
    matfile = fetch_mat_file(id.mat)

    # Initialise Simulation
    simulation = PlotMassSimulation(matfile, id.curvature, int(width), int(height), id.mass, id.power, id.air_density, id.reference_area, id.coefficient_of_drag, id.coefficient_of_friction, id.coefficient_of_lift)
    
    # Pickle graph & stats for download
    simulation.pickle(simulation.plot_speed_curvature(), "graph_curvature.p")

    # Update discord rich presence
    if rpc_activated:
        RPC.update(state= str(int(id.mass)) + 'kg @ ' + str(int(id.power)) + 'W - ' + str(simulation.get_fastest_lap()), details=str(id.name) + ' - Speed v Curvature', large_image="qut-logo")

    return render_template('speedcurvature.html', graph_html=simulation.plot_speed_curvature_html(), title=title, name=id.name, fastest_lap=simulation.get_fastest_lap()[2:], id=id)

# Standard Input page for Roadload Modelling
@bp.route('/accumulator/<id>', defaults={'width': None, 'height': None})
@bp.route('/accumulator/<id>/<width>/<height>')
def accumulator(id, width=None, height=None):
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    if not width or not height:
        return """
        <script>
        (() => window.location.href = window.location.href +
        ['', window.innerWidth, window.innerHeight].join('/'))()
        </script>
        """

    # Fetch lap simulation inputs from database
    id = Lap.query.filter_by(id=id).first()

    # Update page title
    title = 'QUTMS | Accumulator'

    # Fetch pre-existing roadload inputs in database
    roadload_inputs = Accumulator.query.order_by(Accumulator.id.desc()).all()

    # Update discord rich presence
    if rpc_activated:
        RPC.update(state= "A Chunky Accumulator", details='Modelling', large_image="qut-logo")

    return render_template('accumulator.html', name=id.name, id=id, title=title, car_mass=int(id.mass), data=roadload_inputs, dataform=accumulatorForm())

# Graph roadload model
@bp.route('/roadload/<roadload_id>/<lap_id>', defaults={'width': None, 'height': None})
@bp.route('/roadload/<roadload_id>/<lap_id>/<width>/<height>')
def roadload(roadload_id, lap_id, width=None, height=None):
    if not width or not height:
        return """
        <script>
        (() => window.location.href = window.location.href +
        ['', window.innerWidth, window.innerHeight].join('/'))()
        </script>
        """

    # Fetch roadload simulation inputs from database
    accumulator_spec = Accumulator.query.filter_by(id=roadload_id).first()

    # Fetch lap simulation inputs from database
    lap_spec = Lap.query.filter_by(id=lap_id).first()

    # Update page title
    title = 'QUTMS | Roadload'

    # Fetch mat file for simulation input
    matfile = fetch_mat_file(lap_spec.mat)

    # Initialise Lap Simulation
    lap_simulation = PlotMassSimulation(matfile, lap_spec.curvature, int(width), int(height), lap_spec.mass, lap_spec.power, lap_spec.air_density, lap_spec.reference_area, lap_spec.coefficient_of_drag, lap_spec.coefficient_of_friction, lap_spec.coefficient_of_lift)

    # Iterate through lap simulations
    steps = stepped_values(lap_spec.mass)
    lap_product = {}
    for i in steps:
        lap_product[i] = PlotMassSimulation(matfile, lap_spec.curvature, int(width), int(height), i, lap_spec.power, lap_spec.air_density, lap_spec.reference_area, lap_spec.coefficient_of_drag, lap_spec.coefficient_of_friction, lap_spec.coefficient_of_lift)

    # Initialise Roadload Simulation
    roadload_simulation = Roadload(accumulator_spec)
    roadload_simulation.set_simulation_iterations(lap_product)
    roadload_simulation.set_roadload_calcs()

    return render_template('roadload.html', title=title, lap_spec=lap_spec, accumulator_spec=accumulator_spec, lap_sim=lap_simulation, graph_html=roadload_simulation.plot())


# Delete Lap Entry
@bp.route('/lrm/<id>')
def lrm(id):
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
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
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    info = QCAR.query.filter_by(id=id).first()
    QCAR.query.filter_by(id=id).delete()
    db.session.commit()
    flash("File removed" )
    return redirect('/edit')

# Uploads data object for Plot Mass
@bp.route('/data', methods=['GET','POST'])
def data():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    dataform = dataForm()
    if dataform.validate_on_submit():
        db_file_path=check_upload_file(dataform)
        #insert item into database
        newitem = Lap(id = datetime.datetime.now(),
                    name=dataform.name.data,
                    mat = 'track_' + str(mat_upload_number) + '.mat',
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
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
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

# Upload data for Quarter Car
@bp.route('/upload/accumulator', methods=['GET','POST'])
def accumulator_data():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    dataform = accumulatorForm()
    if dataform.validate_on_submit():
        newitem = Accumulator(id = datetime.datetime.now(),
                    name = dataform.name.data,
                    FoS = dataform.FoS.data,
                    regen = float(dataform.regen.data) / 100,
                    cellMass = dataform.cellMass.data,
                    cellCoverMass = dataform.cellCoverMass.data,
                    accumBoxMass = dataform.accumBoxMass.data,
                    vehicleMass = dataform.vehicleMass.data,
                    driverMass = dataform.driverMass.data,
                    rollingResistanceCoefficient = dataform.rollingResistanceCoefficient.data,
                    wheelbase = dataform.wheelbase.data,
                    gradient = dataform.gradient.data,
                    frontAxel = (float(dataform.frontAxel.data) / 100) * dataform.wheelbase.data,
                    rearAxel = (float(dataform.rearAxel.data) / 100) * dataform.wheelbase.data,
                    airVelocity = dataform.airVelocity.data,
                    gearRatio = dataform.gearRatio.data,
                    efficiency = float(dataform.efficiency.data) / 100,
                    wheelRadius = dataform.wheelRadius.data,
                    nominalVoltage = dataform.nominalVoltage.data,
                    cellNominalVoltage = dataform.cellNominalVoltage.data,
                    cellCapacity = dataform.cellCapacity.data
                    )
        #add the object to the db session
        db.session.add(newitem)
        #commit to the database
        db.session.commit()
        flash('The file was successfully uploaded to the database', 'success')
        print('Added', 'success')
    return redirect(url_for('main.accumulator', id=identity))

# download .mat file of stats
@bp.route('/export_mat', methods=['GET', "POST"])
def export_mat():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    statistics = pickle.load(open('statistics.p','rb'))
    savemat('sim/static/mat/statistics.mat',statistics)
    return send_file('static/mat/statistics.mat', as_attachment=True, attachment_filename='statistics.mat')

# download all graphs
@bp.route('/export_button', methods=['GET', "POST"])
def export_generate_all():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    #load pickled graphs
    fig = pickle.load(open('graph_all.p','rb'))
    #save as svg internally
    fig.savefig('sim/static/svg/graph_all.svg')
    # update discord
    if rpc_activated:
        RPC.update(state="Simulations", details="Exporting", large_image="qut-logo")
    #return svg to client
    return send_file('static/svg/graph_all.svg', as_attachment=True, attachment_filename='graph_output_all.svg')   

# download gg graph
@bp.route('/export_button_gg')
def export_generate_gg():
    if current_user.is_anonymous:
        flash('You need to login')
        return redirect('/login')
    #load pickled gg graph
    fig_gg = pickle.load(open('graph_gg.p','rb'))
    #save as svg internally
    fig_gg.savefig('sim/static/svg/graph_gg.svg')
    # update discord
    if rpc_activated:
        RPC.update(state="GG Diagram", details="Exporting", large_image="qut-logo")
    #return svg to client
    return send_file('static/svg/graph_gg.svg', as_attachment=True, attachment_filename='graph_output_gg.svg')

