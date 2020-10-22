from flask import render_template
from app import app
import psycopg2
from flask import jsonify, request

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
    agency_id = request.form['agency_id']
    username = request.form['username']  
    password = request.form['password']  

    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("select admin_id from travel_agency where agency_id = " + agency_id)
    
    admin_rec = cursor.fetchone()
    admin_id = admin_rec[0]
    cursor.execute("select user_id, passcode from administration where admin_id = '" + admin_id + "'")
    user_det_rec = cursor.fetchone()
    user_id = user_det_rec[0] # value of the 1st column in the select statement
    passcode = user_det_rec[1] # value of 2nd column in select statement

    cursor.close()
    connection.close()
    if username == user_id and password == passcode:  
        return jsonify({'success':True})
    else:
        return jsonify({'success':False})
    

@app.route('/getbuses', methods=["GET"])
def getbuses():
    start_station = request.args["start_station"]
    dest = request.args["destination"]
    date_of_tr = request.args["date_of_travel"]

    connection = get_connection()
    cursor = connection.cursor()

    print("select bus_no, start_station, destination, depart_time, seats_left, agency_id, depart_date from bus_info where start_station = '" + start_station + "' and destination = '" + dest + "' and depart_date = '" + date_of_tr + "'")
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

    print("select train_no, train_name, start_station, depart_time, seats_left, destination, agency_id, depart_date from train_info where start_station = '" + start_station + "' and destination = '" + dest + "' and depart_date = '" + date_of_tr + "'")

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
        house_no = request.form['house_no' + str(i)]
        locality = request.form['locality' + str(i)]
        city = request.form['city' + str(i)]
        state = request.form['state' + str(i)]
        pincode = request.form['pincode' + str(i)]

        connection = get_connection()
        cursor = connection.cursor()

        if p_name == "" and adhaar_no == "" and dob == "" and house_no == "" and locality == "" and city == "" and state == "" and pincode == "" and contact == "":
            continue
        else:
            cursor.execute("insert into customer values (" + adhaar_no + ", " + p_name + ", " + dob + ")")
            cursor.execute("insert into address values(" + house_no + ", " + locality + ", " + city + ", " + state + ", " + pincode + ", " + adhaar_no + ")")
            cursor.execute("insert into customer_contact values (" + contact + ", " + adhaar_no + ")")

    cursor.close()
    connection.close()

@app.route('/reserconf', methods=["POST"])
def reserconf():
    for i in range(1, 7):
        adhaar_no = request.form["adhaar_no" + str(i)]
        travel_mode = request.form["travel_mode" + str(i)]
        vehicle_no = request.form["vehicle_no" + str(i)]
        seat_no = request.form["seat_no" + str(i)]

        connection = get_connection()
        cursor = connection.cursor()

        if adhaar_no == "" and travel_mode == "" and vehicle_no == "" and seat_no == "":
            continue
        else:
            cursor.execute("insert into reservation values (" + adhaar_no + ", " + travel_mode + ", " + vehicle_no + ", " + seat_no + ")")
    
    cursor.close()
    connection.close()

@app.route('/payconf', methods=["POST"])
def payconf():
    pass


@app.route('/confdisplay', methods=["GET"])
def confdisplay():
    pass
