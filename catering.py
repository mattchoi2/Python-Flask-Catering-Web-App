"""
	Catering
	~~~~~~

	A catering application

	:copyright: (c) 2019 by Matthew Choi

	RUN INSTRUCTIONS:
	export FLASK_APP=catering.py
    export FLASK_ENV=development
	flask initdb
	flask run
	Install with '''pip3 install flask_sqlalchemy'''
"""

import time
import os
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from models import db, Customer, EventRequest, Owner, Staff, Assignment
from werkzeug import check_password_hash, generate_password_hash
from utils import validate_request, validate_staff_input
from datetime import datetime

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'catering.db')

app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

# configuration
PER_PAGE = 30
DEBUG = True
SECRET_KEY = '123456789'

app.secret_key = SECRET_KEY

db.init_app(app)

@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	db.create_all()
	print('Initialized the database.')
	supreme_overlord = Owner("owner", generate_password_hash("pass"))
	db.session.add(supreme_overlord)
	db.session.commit()


@app.route("/")
def default():
	return redirect(url_for("login"))

@app.route("/login/", methods=["GET", "POST"])
def login():
	error = None
	cust = None
	if 'cust_id' in session: # You can't login twice, go to your main page
		return redirect(url_for('events'))
	if 'owner_id' in session:
		return redirect(url_for('manage'))
	if request.method == "POST":
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['password']:
			error = 'You have to enter a password'
		else:
			cust = Customer.query.filter_by(username=request.form['username']).first()
			owner = Owner.query.filter_by(username=request.form['username']).first()
			staff = Staff.query.filter_by(username=request.form['username']).first()
			if cust == None and owner == None and staff == None:
				error = "Invalid username"
			if cust != None:
				error = login_customer(cust, request.form["password"])
				if error == None:
					return redirect(url_for('events'))
			elif owner != None:
				error = login_owner(owner, request.form["password"])
				if error == None:
					return redirect(url_for('manage'))
			elif staff != None:
				error = login_staff(staff, request.form["password"])
				if error == None:
					return redirect(url_for('staff'))

	return render_template('login.html', error=error)

def login_customer(cust, password):
	if not check_password_hash(cust.pw_hash, password):
		return "Invalid password"
	session['cust_id'] = cust.user_id
	return None

def login_staff(staff, password):
	if not check_password_hash(staff.pw_hash, password):
		return "Invalid password"
	session['staff_id'] = staff.staff_id
	return None

def login_owner(owner, password):
	if not check_password_hash(owner.pw_hash, password):
		return "Invalid password"
	session['owner_id'] = owner.owner_id
	return None

@app.route("/staff/",  methods=["POST", "GET"])
def staff():
	error = None
	if "staff_id" not in session:
		abort(401)
	staff = Staff.query.filter_by(staff_id=session["staff_id"]).first()
	reqs = EventRequest.query.order_by(EventRequest.start_datetime.asc()).all()

	for req in reqs:
		for assignment in req.assignments:
			if staff.staff_id == assignment.staff_id:
				reqs.remove(req) # Take it off the list of requests the staff can sign up for


	return render_template('staff.html', assignments=staff.assignments, requests=reqs, staff=staff, error=error)

@app.route("/register/",  methods=["POST", "GET"])
def register():
	error = None
	if request.method == "POST":
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['password']:
			error = 'You have to enter a password'
		else:
			cust = Customer(request.form['username'], generate_password_hash(request.form['password']))
			db.session.add(cust)
			db.session.commit()
			db.session.flush()

			flash("Welcome " + request.form['username'] + "! ")
			flash("You have successfully registered for an account!")
			session['cust_id'] = cust.user_id # Allows the session to remember user is logged in
	return render_template('register.html', error=error)

@app.route("/logout/",  methods=["GET"])
def logout():
	flash("You have been logged out.")
	session.pop('cust_id', None)
	session.pop('owner_id', None)
	session.pop('staff_id', None)
	return redirect(url_for('login'))

@app.route("/manage/",  methods=["POST", "GET"])
def manage():
	error = None
	if "owner_id" not in session:
		abort(401)
	if request.method == "POST":
		error = validate_staff_input(request.form)
		if error == None:
			staff = Staff(request.form["username"], generate_password_hash(request.form["password"]))
			db.session.add(staff)
			db.session.commit()
			flash("Added new staff " + staff.username + " successfully!")
	reqs = EventRequest.query.order_by(EventRequest.start_datetime.asc()).all()
	owner = Owner.query.filter_by(owner_id=session["owner_id"]).first()
	staffings = {}
	staff = Staff.query.all()
	return render_template("manage.html", requests=reqs, staff=staff, staffings=staffings, user_name=owner.username, error=error)

@app.route("/addStaff/",  methods=["POST"])
def add_staff():
	if "staff_id" not in session:
		abort(401)
	if not request.form["request_id"]:
		abort(404)
	# Get all the data from the single select element value, we need event request id and staff id

	staff = Staff.query.filter_by(staff_id=session["staff_id"]).first()
	eventRequest = EventRequest.query.filter_by(request_id=request.form["request_id"]).first()
	if staff == None or eventRequest == None: # Make sure both exist in the DB, for FK validation
		abort(404)
	assign = Assignment(eventRequest.request_id, staff.staff_id)
	db.session.add(assign)
	db.session.commit()
	flash("Staff " + staff.username + " assigned to event " + str(eventRequest) + " successfully!")
	return redirect(url_for('staff'))

@app.route("/events/",  methods=["POST", "GET"])
def events():
	error = None
	if 'cust_id' not in session:
		abort(401) # Not authorized
	if request.method == "POST":
		error = validate_request(request.form)
		if not error:
			if create_event_request(request.form):
				flash("Successfully added '" + request.form["eventName"] + "' event!")
			else:
				error = "Unfortunately, we are already booked for that date.  An existing event request overlaps with the requested times."
	# Get the user
	cust = Customer.query.filter_by(user_id=session['cust_id']).first()
	reqs = EventRequest.query.filter_by(user_id=session['cust_id']).order_by(EventRequest.start_datetime.asc()).all()
	if not cust:
		abort(404)
	return render_template("events.html", error=error, user_name=cust.username, requests=reqs)

@app.route("/deleteEventRequest/<request_id>",  methods=["GET"])
def delete_event_request(request_id):
	if 'cust_id' not in session:
		abort(401) # Not authorized
	req = EventRequest.query.filter_by(request_id=request_id).first()
	db.session.delete(req)
	db.session.commit()
	return redirect(url_for('events'))

def create_event_request(form):
	inputStartDatetime = form["startDate"] + " " + form["beginTime"]
	inputEndDatetime = form["endDate"] + " " + form["endTime"]
	# Will be in the form "Oct 16, 2019 07:13 PM"
	beginDatetime = datetime.strptime(inputStartDatetime, '%b %d, %Y %I:%M %p')
	endDatetime = datetime.strptime(inputEndDatetime, '%b %d, %Y %I:%M %p')
	newReq = EventRequest(form["eventName"], beginDatetime, endDatetime, session["cust_id"])
	for req in EventRequest.query.all():
		# Check to see if any existing event requests overlap with the new one
		if newReq.start_datetime.date() <= req.end_datetime.date() and newReq.end_datetime.date() >= req.start_datetime.date():
			return False

	# Add the new event request to the DB!
	db.session.add(newReq)
	db.session.commit()
	return True
