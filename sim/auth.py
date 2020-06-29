from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm,forgetForm,changeForm
from flask_login import login_user,current_user,logout_user, login_required
from . import db


bp = Blueprint('auth', __name__)
secrect = 'm0TER-sP0RTS'

#routing for login
@bp.route('/login')
def login():
    login_form = LoginForm()
    return render_template('login.html', login_form = login_form)

@bp.route('/forget')
def forget():
    forgetpwd = forgetForm()
    return render_template('forget.html', forget = forgetpwd)

@bp.route('/check', methods = ['POST'])
def check():
    forgetpwd = forgetForm()
    if forgetpwd.validate_on_submit():
        #get email,password and email from the form
        email = forgetpwd.email.data
        find = User.query.filter_by(email=email).first()
        if find != 'None':
               return redirect(url_for('auth.change_password', email = email))
        else: 
            flash('this email is not registered')
            return redirect(url_for('auth.forget'))

@bp.route('/changepwd')
def change_password():
    change = changeForm()
    email = request.args.get('email')

    return render_template('change.html', change=change, email=email)

@bp.route('/updatepwd/<email>', methods = ['POST'])
def updatepwd(email):
    change = changeForm()
    if change.validate_on_submit():
        password = change.password.data
        hashWord = generate_password_hash(password+email+secrect)
        db.session.query(User).filter_by(email=email).update({User.password_hash:hashWord})
        db.session.commit()
        flash('password updated')
        return redirect(url_for('auth.login'))




#this is the login function
@bp.route('/log', methods = ['POST'])
def log():
    login_form=LoginForm()
    error=None
    if(login_form.validate_on_submit()):
        email = login_form.email.data
        password = login_form.password.data
        u1 = User.query.filter_by(email = email).first()

        if u1 is None:
            error='Incorrect email'
            flash(error)
            print(error)
        elif not check_password_hash(u1.password_hash,password+email+secrect):
            error='Incorrect Password'
            flash(error)
            print(error)
        if error is None:
            print(u1)
            login_user(u1)
            flash('Welcome! ' + u1.email)
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
        #get email,password and email from the form
        email = registerform.email.data
        password = registerform.password.data

        #create password hash
        hashWord = generate_password_hash(password+email+secrect)

        #create a new user account
        try: 
            newUser = User(email=email, password_hash=hashWord)
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except:
            flash("Looks like the email had been used, try another one!" )
            return redirect(url_for('auth.reg'))
    else: 
        flash('passwords must match')
        return redirect(url_for('auth.reg'))