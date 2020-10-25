from flask import render_template, session
from app import app

@app.route('/')
def index():
    return render_template("public/index.html")

@app.route('/trains_buses')
def trains_buses():
    return render_template('public/trainOrBus.html')

@app.route('/get_buses')
def get_buses():
    return render_template('public/selectBus.html')

@app.route('/get_trains')
def get_trains():
    return render_template('public/selectTrain.html')

@app.route('/passenger_details')
def passenger_details():
    return render_template('public/passengerDetails.html')

@app.route('/booking_confirmation')
def booking_confirmation():
    return render_template('public/bookingConf.html', adhaar_no1 = '123456789134')

@app.route('/payment_confirmation')
def payment_confirmation():
    return render_template('public/paymentConf.html', **session)

@app.route('/view_booking')
def view_booking():
    return render_template('public/viewBooking.html', **session)