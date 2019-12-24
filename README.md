# Python Flask Catering Web App

## Visualizations:

Login page:
![Image of Login Page](https://github.com/mattchoi2/Python-Flask-Catering-Web-App/blob/master/images/login.PNG?raw=true)

Create an event as a customer:
![Image of Create Event Page](https://github.com/mattchoi2/Python-Flask-Catering-Web-App/blob/master/images/createEvent.PNG?raw=true)

Signup as a staff for an event:
![Image of Staff Signup Page](https://github.com/mattchoi2/Python-Flask-Catering-Web-App/blob/master/images/staff.PNG?raw=true)

Manage events and staff as admin:
![Image of Admin Management](https://github.com/mattchoi2/Python-Flask-Catering-Web-App/blob/master/images/owner.PNG?raw=true)

## Goal:
To gain experience using Flask and building data models via an ORM by developing a website to help manage a catering company.

## High-level description:
You will be writing a website to help manage a catering company.  To accomplish
this, you will need to consider three classes of users:  the owner of the
company, company staff, and registered customers.  Customers will request
events on given days (or cancel events they had previously requested), staff
will sign up to work events, and the owner will given a rundown of what events
are scheduled and who is working each event.  The company cannot schedule more
than 1 event per day, and each event needs only 3 Staff members to run.

## Specifications:
1.  You must build your website using Python, Flask, SQLAlchemy, and the Flask-SQLAlchemy extension.
1.  Managing users
	*  Each user (Owner, Staff, or Customer) should have a username and password.
	*  Customers are free to register for their own account.
	*  Staff accounts must be created by the Owner (it is fine for the Owner to set passwords for the Staff).
	*  If a user is logged in, no matter what page they are on, they should have access to a logout link.
1.  Owner
	*  Should be able to login with the username "owner" and password "pass".
	*  Once logged in, the Owner should be presented with a link to create new staff accounts, and a list of all scheduled events.
		*  For each event, the Staff members signed up to work that event should be listed.
		*  If no events are scheduled, a message should be displayed informing the Owner of this explicitly.
		*  If any scheduled event has no staff signed up to work, a message should be displayed informing the Owner of this explicitly.
1.  Staff
	*  Once logged in, Staff members should be presented with a list of events they are scheduled to work and a list of events that they can sign up to work.
		*  For each event that a Staff member can sign up to work, they should be provided a link to sign up for that event.
		*  No event that already has 3 Staff members signed up to work should be presented as a sign up option for other Staff members.
1.  Customers
	*  Once logged in, Customers should be presented with a form to request a new event, and a list of events they have already requested.
		*  If a Customer requests an event on a date when another event is already scheduled, they should be presented with an message saying that the company is already booked for that date.
		*  For each requested event, the Customer should be provided with a link to cancel that event.
1.  Data management
	*  To ease bootstrapping and testing of your application, hardcode the Owner's username and password in your app to be "owner" and "pass".
	*  All other data for your application should be stored in an SQLite database named "catering.db" using SQLAlchemy's ORM and the Flask-SQLAlchemy extension.
