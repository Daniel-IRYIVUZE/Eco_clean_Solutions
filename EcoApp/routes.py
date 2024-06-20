from flask import render_template, flash, url_for, redirect, request, abort
from EcoApp import app, db, bcrypt
from EcoApp.form import RegisterForm, LoginForm,ServiceForm
from EcoApp.model import Users,Services, Order, OrderServices
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
    users = Users.query.filter(Users.email != "admin@gmail.com").all()
    orders= Order.query.filter_by(status="pending").all()
    ordersNumber= len(orders)
    usersNumber= len(users)
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)
    return render_template("admin-dash.html", number=usersNumber)

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.route("/admin/customers")
@login_required
def customers():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)
    users = Users.query.filter(Users.email != "admin@gmail.com").all()
    return render_template("customers.html", users=users)

@app.route("/admin/report")
@login_required
def report():
    return render_template("adminrepo.html")

@app.route("/book/<service_name>", methods=["GET", "POST"])
@login_required
def book(service_name):
    form = ServiceForm()
    service = Services.query.filter_by(service_name=service_name).first()
    
    if not service:
        flash("Service not found", "danger")
        return redirect(url_for('index'))
    
    name = service.service_name
    form.serviceName.data = name
    form.price.data = service.price
    
    if request.method == "POST" and form.validate_on_submit():
        # Create a new order
        new_order = Order(
            user_id=current_user.id,
            scheduled_date=form.date.data,
            status='Pending'
        )
        db.session.add(new_order)
        db.session.commit()
        
        # Create an entry in the OrderServices table
        order_service = OrderServices(
            order_id=new_order.id,
            service_id=service.id
        )
        db.session.add(order_service)
        db.session.commit()
        
        flash("Your order has been placed successfully", "success")
        return redirect(url_for('index'))
    
    time = {
        "Junky Removal": "9am to 11 am",
        "Secure Destruction": "3pm to 5pm",
        "Residential Recycling": "1pm to 3pm"
    }.get(name, "9am to 5pm")

    return render_template("booking.html", form=form, time=time)
