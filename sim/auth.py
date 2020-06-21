from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user,current_user,logout_user, login_required
from . import db

#create a blueprint
bp = Blueprint('auth', __name__)

secrect = 'm0TER-sP0RTS'

#routing for login
@bp.route('/login')
def login():
    login_form = LoginForm()
    return render_template('login.html', login_form = login_form)

#this is the login function
@bp.route('/log', methods = ['POST'])
def log():
    login_form=LoginForm()
    error=None
    if(login_form.validate_on_submit()):
        username = login_form.username.data
        password = login_form.password.data
        u1 = User.query.filter_by(name = username).first()

        if u1 is None:
            error='Incorrect Username'
            flash(error)
            print(error)
        elif not check_password_hash(u1.password_hash,password+username+secrect):
            error='Incorrect Password'
            flash(error)
            print(error)
        if error is None:
            print(u1)
            login_user(u1)
            flash('Welcome! ' + u1.name)
            return redirect(url_for('main.home'))
        else:
            return redirect(url_for('auth.login'))

@bp.route("/logout")
def logout():
    if current_user.is_anonymous:
        return redirect('/login')
    else:
        print(current_user)

    logout_user()
    return redirect(url_for('main.home'))


@bp.route('/reg')
def reg():
    registerform = RegisterForm()
    return render_template('register.html',registerform = registerform)

@bp.route('/register', methods = ['POST'])
def register():
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        #get username,password and email from the form
        username = registerform.username.data
        password = registerform.password.data

        #create password hash
        hashWord = generate_password_hash(password+username+secrect)

        #create a new user account
        try: 
            newUser = User(name=username, password_hash=hashWord)
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except:
            flash("Looks like the username had been used, try another one!" )
            return redirect(url_for('auth.reg'))
    else: 
        flash('passwords must match')
        return redirect(url_for('auth.reg'))