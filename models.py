from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Customer(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), nullable=False)
	pw_hash = db.Column(db.String(64), nullable=False)

	def __init__(self, username, pw_hash):
		self.username = username
		self.pw_hash = pw_hash

	def __repr__(self):
		return '<Customer {}>'.format(self.username)

class EventRequest(db.Model):
	__tablename__ = "eventrequest"
	request_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), nullable=False)
	start_datetime = db.Column(db.DateTime(), nullable=False)
	end_datetime = db.Column(db.DateTime(), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('customer.user_id'), nullable=False)
	assignments = db.relationship("Assignment")

	def __init__(self, name, start_datetime, end_datetime, user_id):
		self.name = name
		self.start_datetime = start_datetime
		self.end_datetime = end_datetime
		self.user_id = user_id

	def __repr__(self):
		return self.name

class Owner(db.Model):
	owner_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), nullable=False)
	pw_hash = db.Column(db.String(64), nullable=False)

	def __init__(self, username, pw_hash):
		self.username = username
		self.pw_hash = pw_hash

class Staff(db.Model):
	staff_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), nullable=False)
	pw_hash = db.Column(db.String(64), nullable=False)
	assignments = db.relationship("Assignment")

	def __init__(self, username, pw_hash):
		self.username = username
		self.pw_hash = pw_hash

class Assignment(db.Model):
	assignment_id = db.Column(db.Integer, primary_key=True)
	request_id = db.Column(db.Integer, db.ForeignKey("eventrequest.request_id"))
	staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))

	staff = db.relationship("Staff", back_populates="assignments")
	request = db.relationship("EventRequest", back_populates="assignments")

	def __init__(self, request_id, staff_id):
		self.request_id = request_id
		self.staff_id = staff_id

	def __repr__(self):
		return self.staff.username + " is assigned to event " + self.request.name + " | " + self.request.start_datetime.strftime('%d %b, %Y') + " - " + self.request.start_datetime.strftime('%I:%M %p') + " to " + self.request.end_datetime.strftime('%d %b, %Y') + " - " + self.request.end_datetime.strftime('%I:%M %p')

# class User(db.Model):
# 	user_id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(24), nullable=False)
# 	email = db.Column(db.String(80), nullable=False)
# 	pw_hash = db.Column(db.String(64), nullable=False)
#
# 	messages = db.relationship('Message', backref='author')
#
# 	# because this relationship does NOT include another table, you must specify how to join
# 	follows = db.relationship('User', secondary='follows', # uses the table follows to connect the two users
# 		primaryjoin='User.user_id==follows.c.follower_id',
# 		secondaryjoin='User.user_id==follows.c.followee_id',
# 		backref=db.backref('followed_by', lazy='dynamic'), lazy='dynamic')
#
# 	def __init__(self, username, email, pw_hash):
# 		self.username = username
# 		self.email = email
# 		self.pw_hash = pw_hash
#
# 	def __repr__(self):
# 		return '<User {}>'.format(self.username)
#
# follows = db.Table('follows',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.user_id')),
#     db.Column('followee_id', db.Integer, db.ForeignKey('user.user_id'))
# )
#
# class Message(db.Model):
# 	message_id = db.Column(db.Integer, primary_key=True)
# 	author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
# 	text = db.Column(db.Text, nullable=False)
# 	pub_date = db.Column(db.Integer)
#
# 	def __init__(self, author_id, text, pub_date):
# 			self.author_id = author_id
# 			self.text = text
# 			self.pub_date = pub_date
#
# 	def __repr__(self):
# 			return '<Message {}'.format(self.message_id)
