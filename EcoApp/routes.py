from flask import render_template, flash, url_for, redirect, request
from EcoApp import app, db, bcrypt
from EcoApp.form import RegisterForm, LoginForm
from EcoApp.model import Users, Company, Services, Order
from flask_login import login_user, current_user, logout_user

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = Users(
            first_name=form.firstname.data,
            last_name=form.lastname.data,
            email=form.email.data,
            password=hashed_pw,
            district=form.district.data,
            sector=form.sector.data,
            village=form.village.data,
            street=form.street.data,
            cell=form.cell.data
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account was successfully created, you can log in now", 'success')
        return redirect(url_for("login"))
    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))  # Redirect to a valid route
        else:
            flash("Log in unsuccessful. Check your email and password", 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
