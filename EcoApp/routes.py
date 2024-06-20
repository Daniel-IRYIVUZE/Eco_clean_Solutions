from flask import render_template, flash, url_for, redirect, request, abort, jsonify
from EcoApp import app, db, bcrypt
from EcoApp.form import RegisterForm, LoginForm, ServiceForm, RangeTime,ProfileForm
from EcoApp.model import Users, Services, Order, OrderServices
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

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
    next_page= request.args.get("next")  
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if next_page:    
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash("Log in unsuccessful. Check your email and password", 'warning')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/admin")
@login_required
def admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)
    
    users = Users.query.filter(Users.email != "admin@gmail.com").all()
    ordersReq = Order.query.filter_by(status="Pending").all()  
    
    usersNumber = len(users)
    ordersReqNumber = len(ordersReq)
    
    return render_template("admin-dash.html", number=usersNumber, reqnumber=ordersReqNumber, ordersReq=ordersReq)

@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html',error=error), 403

@app.errorhandler(404)
def forbidden(error):
    return render_template('error.html',error=error), 404

@app.route("/admin/customers")
@login_required
def customers():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)
    users = Users.query.filter(Users.email != "admin@gmail.com").all()
    return render_template("customers.html", users=users)

@app.route("/admin/report", methods=["GET", "POST"])
@login_required
def report():
    form = RangeTime()
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)

    # Initialize the form with current dates only on GET request
    if request.method == 'GET':
        form.datefrom.data = datetime.now().date()  
        form.dateto.data = datetime.now().date() 

    if form.validate_on_submit():
       
        date_from = datetime.strptime(form.datefrom.data, "%Y-%m-%d").date()
        date_to = datetime.strptime(form.dateto.data, "%Y-%m-%d").date()

        # Fetch orders based on the selected date range
        ordersReq = Order.query.filter(Order.status == "Completed", 
                                       Order.scheduled_date.between(date_from, date_to)).all()
    else:
        ordersReq = Order.query.filter_by(status="Completed").all()

    usersNumber = len(Users.query.filter(Users.email != "admin@gmail.com").all())
    ordersReqNumber = len(ordersReq)

    return render_template("adminrepo.html", ordersReq=ordersReq, number=usersNumber, reqnumber=ordersReqNumber, form=form)

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

@app.route('/update-order-status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    new_status = request.json.get('status')

    # Perform database update logic here
    order = Order.query.get(order_id)
    if order:
        order.status = new_status
        db.session.commit()
        return jsonify({'message': 'Status updated successfully'}), 200
    else:
        return jsonify({'message': 'Order not found'}), 404


@app.route("/dashboard")
@login_required
def user_dash():
    declined_orders = Order.query.filter(Order.user_id == current_user.id, Order.status == "Declined").all()
    declined_nber= len(declined_orders)
     
    completed_orders = Order.query.filter(Order.user_id == current_user.id, Order.status == "Completed").all()
    completed_nber=len(completed_orders)

    current_orders= current_user.orders

    return render_template("user-dash.html", declined_nber=declined_nber, completed_nber=completed_nber, current_orders= current_orders)
   

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = ProfileForm()
    if form.validate_on_submit():
        # Verify the current password
        if not bcrypt.check_password_hash(current_user.password, form.current_password.data):
            flash("Current password is incorrect", "danger")
            return redirect(url_for("settings"))
        
        # Update user details
        current_user.first_name = form.firstname.data
        current_user.last_name = form.lastname.data
        current_user.email = form.email.data
        current_user.district = form.district.data
        current_user.village = form.village.data
        current_user.sector = form.sector.data
        current_user.cell = form.cell.data
        current_user.street = form.street.data
        
        # Update password if a new one is provided
        if form.password.data:
            current_user.password = bcrypt.generate_password_hash(form.password.data)
        
        db.session.commit()
        flash("Your Profile info was successfully updated", "success")
        return redirect(url_for("settings"))
    
    elif request.method == "GET":
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name
        form.email.data = current_user.email
        form.district.data = current_user.district
        form.village.data = current_user.village
        form.sector.data = current_user.sector
        form.cell.data = current_user.cell
        form.street.data = current_user.street
    return render_template('settings.html', form=form)




