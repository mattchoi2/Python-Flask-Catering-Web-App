
from datetime import datetime

def validate_request(form):
    error = None
    if not form["eventName"]:
        error = "Enter the event name"
    elif not form["startDate"]:
        error = "Enter the start date"
    elif not form["endDate"]:
        error = "Enter the end date"
    elif not form["beginTime"]:
        error = "Enter the begin time"
    elif not form["endTime"]:
        error = "Enter the end time"

    if not error:
        inputStartDatetime = form["startDate"] + " " + form["beginTime"]
        inputEndDatetime = form["endDate"] + " " + form["endTime"]
        # Will be in the form "Oct 16, 2019 07:13 PM"
        beginDatetime = datetime.strptime(inputStartDatetime, '%b %d, %Y %I:%M %p')
        endDatetime = datetime.strptime(inputEndDatetime, '%b %d, %Y %I:%M %p')

        if beginDatetime > endDatetime: # You can't have a begin time LATER than the end time
            error = "The begin date of '" + str(beginDatetime) + "' is later than the end date entered '" + str(endDatetime) + "'"

    return error

def validate_staff_input(form):
    error = None
    if not form["username"]:
        error = "Enter a username"
    elif not form["password"]:
        error = "Enter a password"
    return error
