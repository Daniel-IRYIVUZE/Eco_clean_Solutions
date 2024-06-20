from flask import render_template, flash, url_for, redirect, request, abort
from EcoApp import app, db, bcrypt
from EcoApp.form import RegisterForm, LoginForm
from EcoApp.model import Users, Company, Services, Order
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    super_pwd = "be738ea88d354ba7ad6a637de0d100353a2f8cca52cf85d213399d52b39edba4"
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        is_admin = True if form.password.data == super_pwd else False
        user = Users(
            first_name=form.firstname.data,
            last_name=form.lastname.data,
            email=form.email.data,
            password=hashed_pw,
            district=form.district.data,
            sector=form.sector.data,
            village=form.village.data,
            street=form.street.data,
            cell=form.cell.data,
            is_admin=is_admin
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account was successfully created, you can log in now", 'success')
        return redirect(url_for("login"))
    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash("Log in unsuccessful. Check your email and password", 'warning')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def user_dash():
    return render_template("user-dash.html")

@app.route("/admin")
@login_required
def admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)
    return render_template("admin-dash.html")

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.route("/admin/customers")
@login_required
def customers():
    return render_template("customers.html")

@app.route("/admin/report")
@login_required
def report():
    return render_template("adminrepo.html")
