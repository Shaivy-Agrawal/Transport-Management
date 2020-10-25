from flask import render_template
from app import app
import psycopg2
from flask import jsonify, request, session
from datetime import date

def get_connection():
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "transportmanagement",
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "transport_management2")
        return (connection)

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        return None

@app.route('/checksignin', methods=["POST"])
def checksignin():  
    agency_id = str(request.form['agency_id'])
    username = str(request.form['username'])  
    password = request.form['password']  

    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("select admin_id from travel_agency where agency_id = " + agency_id)
    
    admin_rec = cursor.fetchone()
    admin_id = admin_rec[0]
    cursor.execute("select user_id, passcode from administration where admin_id = " + admin_id)
    user_det_rec = cursor.fetchone()
    user_id = user_det_rec[0] # value of the 1st column in the select statement
    passcode = user_det_rec[1] # value of 2nd column in select statement

    cursor.close()
    connection.close()
    if username == user_id and password == passcode: 
        session["agency_id"] = agency_id 
        return jsonify({'success':True})
    else:
        return jsonify({'success':False})

@app.route('/getbuses', methods=["GET"])
def getbuses():
    start_station = request.args["start_station"]
    dest = request.args["destination"]
    date_of_tr = request.args["date_of_travel"]

    session["date_of_tr"] = date_of_tr
    session["dest"] = dest
    session["travel_mode"] = "bus"

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("select bus_no, start_station, destination, depart_time, seats_left, agency_id, depart_date from bus_info where start_station = '" + start_station + "' and destination = '" + dest + "' and depart_date = '" + date_of_tr + "'")
    results = cursor.fetchall()

    bus_list = []

    for result in results:
        temp_dict = dict()
        # result: (1, .., .., ..)
        temp_dict["bus_no"] = result[0]
        temp_dict["start_station"] = result[1]
        temp_dict["destination"] = result[2]
        temp_dict["depart_time"] = result[3]
        temp_dict["seats_left"] = result[4]
        temp_dict["agency_id"] = result[5]
        temp_dict["depart_date"] = result[6]

        bus_list.append(temp_dict)

    bus_list_dict = {'Buses': bus_list}

    cursor.close()
    connection.close()
    
    return jsonify(bus_list_dict)

@app.route('/gettrains', methods=["GET"])
def gettrains():
    start_station = request.args["start_station"]
    dest = request.args["destination"]
    date_of_tr = request.args["date_of_travel"]

    session["date_of_tr"] = date_of_tr
    session["dest"] = dest

    session["travel_mode"] = "train"

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("select train_no, train_name, start_station, depart_time, seats_left, destination, agency_id, depart_date from train_info where start_station = '" + start_station + "' and destination = '" + dest + "' and depart_date = '" + date_of_tr + "'")
    results = cursor.fetchall()

    train_list = []

    for result in results:
        temp_dict = dict()
        # result: (1, .., .., ..)
        temp_dict["train_no"] = result[0]
        temp_dict["train_name"] = result[1]
        temp_dict["start_station"] = result[2]
        temp_dict["depart_time"] = result[3]
        temp_dict["seats_left"] = result[4]
        temp_dict["destination"] = result[5]
        temp_dict["agency_id"] = result[6]
        temp_dict["depart_date"] = result[7]

        train_list.append(temp_dict)

    train_list_dict = {'Trains': train_list}

    cursor.close()
    connection.close()

    return jsonify(train_list_dict)

@app.route('/pass_det', methods=["POST"])
def pass_det():
    for i in range(1, 7):
        p_name = request.form['p_name' + str(i)]
        adhaar_no = request.form['adhaar_no' + str(i)]
        dob = request.form['dob' + str(i)]
        contact = request.form['contact' + str(i)]
        house_no = str(request.form['house_no' + str(i)])
        locality = request.form['locality' + str(i)]
        city = request.form['city' + str(i)]
        state = request.form['state' + str(i)]
        pincode = str(request.form['pincode' + str(i)])
        
        session["adhaar_no" + str(i)] = adhaar_no

        connection = get_connection()
        cursor = connection.cursor()

        if p_name == "" and adhaar_no == "" and dob == "" and house_no == "" and locality == "" and city == "" and state == "" and pincode == "" and contact == "":
            continue
        else:
            cursor.execute("insert into customer values ('" + adhaar_no + "', '" + p_name + "', '" + dob + "')")
            cursor.execute("insert into address values(" + house_no + ", '" + locality + "', '" + city + "', '" + state + "', " + pincode + ", '" + adhaar_no + "')")
            cursor.execute("insert into customer_contact values ('" + contact + "', '" + adhaar_no + "')")

    cursor.close()
    connection.close()

@app.route('/reserconf', methods=["POST"])
def reserconf():
    for i in range(1, 7):
        travel_mode = session["travel_mode"]
        vehicle_no = request.form["vehicle_no" + str(i)]
        seat_no = str(request.form["seat_no" + str(i)])

        connection = get_connection()
        cursor = connection.cursor()

        if travel_mode == "" and vehicle_no == "" and seat_no == "":
            session["res_id" + str(i)] = ""
            continue
        else:
            cursor.execute("insert into reservation(start_date, travel_mode, vehicle_no, adhaar_no, destination, agency_id, seat_no) values ('" + session["date_of_tr"] + "', '" + travel_mode + "', '" + vehicle_no + "', '" + session["adhaar_no" + str(i)] + "', '" + session["dest"] + "', " + session["agency_id"] + ", " + seat_no + ") returning res_id")
            new_id = cursor.fetchone()[0]
            session["res_id" + str(i)] = str(new_id)

    cursor.close()
    connection.close()

    res_list = [session["res_id" + str(i)] for i in range(1, 7)]

    return jsonify(res_list)

@app.route('/payconf', methods=["POST"])
def payconf():
    for i in range(1, 7):
        payment_id = str(request.form["payment_id" + str(i)])
        amount = str(request.form["amount" + str(i)])

        session["payment_id" + str(i)] = payment_id

        connection = get_connection()
        cursor = connection.cursor()

        if payment_id == "" and amount == "" and session["res_id" + str(i)] == "":
            continue
        else:
            p_date = date.today().strftime("%Y-%m-%d")
            cursor.execute("insert into payment values (" + session["payment_id" + str(i)] + ", " + str(amount) + ", '" + p_date + "', '" + session["adhaar_no" + str(i)] + "', " + session["res_id" + str(i)] +")")

    cursor.close()
    connection.close()

    res_list = [session["res_id" + str(i)] for i in range(1, 7)]

    return jsonify(res_list)

@app.route('/confdisplay', methods=["GET"])
def confdisplay():
    connection = get_connection()
    cursor = connection.cursor()

    det_list = []

    for i in range(1, 7):
        cursor.execute("select vehicle_no, seat_no, travel_mode from reservation where res_id = " + session["res_id" + str(i)] + " and start_date = '" + session["date_of_tr"] + "' and adhaar_no = '" + session["adhaar_no" + str(i)] + "' and destination = '" + session["dest"] + "' and agency_id = " + session["agency_id"])
        results = cursor.fetchone()

        temp_dict = dict()

        temp_dict["vehicle_no"] = results[0]
        temp_dict["seat_no"] = results[1]
        temp_dict["travel_mode"] = results[2]
        temp_dict["res_id"] = session["res_id" + str(i)]
        temp_dict["payment_id"] = session["payment_id" + str(i)]
        temp_dict["start_date"] = session["date_of_tr"]
        temp_dict["adhaar_no"] = session["adhaar_no" + str(i)]
        temp_dict["destination"] = session["dest"]
        temp_dict["agency_id"] = session["agency_id"]

        det_list.append(det_list)

    return jsonify({'Details': det_list})