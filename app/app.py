#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 14:53:11 2022

@author: chenweixi petertian
"""
from flask import Flask, request, render_template
from bson.json_util import dumps
from pymongo import MongoClient
from urllib.parse import parse_qs
import os


client = MongoClient(host="localhost", port=27017)


# Select the database
db = client.mydb
# Select the collection
collection = db.data


app = Flask(__name__)

picFolder = os.path.join('static', 'pics')

app.config['UPLOAD_FOLDER'] = picFolder

def parse_query_params(query_string):
    """
        Function to parse the query parameter string.
        """
    # Parse the query param string
    query_params = dict(parse_qs(query_string))
    # Get the value from the list
    query_params = {k.decode(): v[0].decode() for k, v in query_params.items()}
    return query_params

@app.route("/", methods = ['GET'])
def home():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'dhl-logo2.svg')
    return render_template("dashboard.html", user_image = pic1)


@app.route('/query1', methods=['GET'])
def query1():
    return render_template('query1.html')


@app.route("/query1",methods = ['POST'])
def get_given_actual_carrier():
    actual_mode = request.form['actual_mode']
    try:
        if collection.count_documents({'actual_mode':actual_mode}) >0:
            # fetch customers by query parameters
            records_fetched = collection.find({'actual_mode':actual_mode}).limit(100)
            user = eval(dumps(records_fetched))
            return render_template('query1.2.html', users=user)
        else:
            return 'No records are found', 404

    except Exception as e:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return e, 500

@app.route('/delete_dashboard', methods=['GET'])
def query2_dashboard():
    return render_template('query2_dashboard.html')

@app.route('/delete_dashboard/weight', methods=['GET'])
def query2_weight():
    return render_template('delete_weight.html')
            
@app.route("/delete_dashboard/weight", methods=['POST'])
def remove_by_weight():
    """
       Function to remove data by weight.
       """
    weight = request.form['weight']
    try:
        # Delete the user
        delete_record = collection.delete({"weight":weight})

        print(delete_record.raw_result)
        if delete_record.deleted_count > 0 :
            # Prepare the response
            return 'Deleted successfully'
        else:
            # Resource not found
            return 'Record not found', 404
    except Exception as e:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        print(e)
        return "", 500
    
@app.route('/delete_dashboard/customer', methods=['GET'])
def query2_customer():
    return render_template('delete_customer.html')
            
@app.route("/delete_dashboard/customer", methods=['POST'])
def remove_by_customer():
    """
       Function to remove data by customer.
       """
    customer = request.form['customer']
    try:
        # Delete the user
        delete_record = collection.delete_many({"customer":customer})

        print(delete_record.raw_result)
        if delete_record.deleted_count > 0 :
            # Prepare the response
            return 'Deleted successfully'
        else:
            # Resource not found
            return 'Record not found', 404
    except Exception as e:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        print(e)
        return "", 500
    
@app.route('/delete_dashboard/cases', methods=['GET'])
def query2_cases():
    return render_template('delete_cases.html')
            
@app.route("/delete_dashboard/cases", methods=['POST'])
def remove_by_cases():
    """
       Function to remove data by cases.
       """
    cases = request.form['cases']
    try:
        # Delete the user
        delete_record = collection.delete_many({"cases":cases})

        print(delete_record.raw_result)
        if delete_record.deleted_count > 0 :
            # Prepare the response
            return 'Deleted successfully'
        else:
            # Resource not found
            return 'Record not found', 404
    except Exception as e:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        print(e)
        return "", 500
    
@app.route('/delete_dashboard/distance', methods=['GET'])
def query2_distance():
    return render_template('delete_distance.html')
            
@app.route("/delete_dashboard/distance", methods=['POST'])
def remove_by_distance():
    """
       Function to remove data by distance.
       """
    distance = request.form['distance']
    try:
        # Delete the user
        delete_record = collection.delete_many({"distance":distance})

        print(delete_record.raw_result)
        if delete_record.deleted_count > 0 :
            # Prepare the response
            return 'Deleted successfully'
        else:
            # Resource not found
            return 'Record not found', 404
    except Exception as e:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        print(e)
        return "", 500

@app.route('/update_dashboard', methods=['GET'])
def query3_dashboard():
    return render_template('query3_dashboard.html')

@app.route('/update_dashboard/case', methods=['GET'])
def query3_case():
    return render_template('query3_case.html')


@app.route("/update_dashboard/case", methods=['POST'])
def update_cases():
    '''
       Function to update  certain customer's cases information
    '''
    customer = request.form['customer']
    value = request.form['cases']
    try:
        # Updating the user
        records_updated = collection.update_many({'customer': customer},{'$set':{'cases' :value}})

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            records_fetched_case = collection.find({'customer':customer}).limit(100)
            user = eval(dumps(records_fetched_case))
            return render_template('query1.2.html', users=user)
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return 'Such Customer is not recorded in database'
    except Exception as e:
        # Error while trying to update the resource
        # Add message for debugging purpose
        print(e)
        return 'Server error', 500
    
@app.route('/update_dashboard/weight', methods=['GET'])
def query3_weight():
    return render_template('query3_weight.html')


@app.route("/update_dashboard/weight", methods=['POST'])
def update_weight():
    '''
       Function to update  certain customer's weight information
    '''
    customer = request.form['customer']
    value = request.form['weight']
    try:
        # Updating the user
        records_updated = collection.update_many({'customer': customer},{'$set':{'weight' :value}})

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            records_fetched_case = collection.find({'customer':customer}).limit(100)
            user = eval(dumps(records_fetched_case))
            return render_template('query1.2.html', users=user)
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return 'Such Customer is not recorded in database'
    except Exception as e:
        # Error while trying to update the resource
        # Add message for debugging purpose
        print(e)
        return 'Server error', 500
    
@app.route('/update_dashboard/distance', methods=['GET'])
def query3_distance():
    return render_template('query3_distance.html')


@app.route("/update_dashboard/distance", methods=['POST'])
def update_distance():
    '''
       Function to update  certain customer's distance information
    '''
    customer = request.form['customer']
    value = request.form['distance']
    try:
        # Updating the user
        records_updated = collection.update_many({'customer': customer},{'$set':{'distance' :value}})

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            records_fetched_case = collection.find({'customer':customer}).limit(100)
            user = eval(dumps(records_fetched_case))
            return render_template('query1.2.html', users=user)
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return 'Such Customer is not recorded in database'
    except Exception as e:
        # Error while trying to update the resource
        # Add message for debugging purpose
        print(e)
        return 'Server error', 500
    
@app.route('/update_dashboard/volume', methods=['GET'])
def query3_volume():
    return render_template('query3_volume.html')


@app.route("/update_dashboard/volume", methods=['POST'])
def update_volume():
    '''
       Function to update  certain customer's volume information
    '''
    customer = request.form['customer']
    value = request.form['volume']
    try:
        # Updating the user
        records_updated = collection.update_many({'customer': customer},{'$set':{'volume' :value}})

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            records_fetched_case = collection.find({'customer':customer}).limit(100)
            user = eval(dumps(records_fetched_case))
            return render_template('query1.2.html', users=user)
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return 'Such Customer is not recorded in database'
    except Exception as e:
        # Error while trying to update the resource
        # Add message for debugging purpose
        print(e)
        return 'Server error', 500
    
@app.route('/fetch', methods=['GET'])
def query4():
    return render_template('query4.html')

@app.route("/fetch",methods = ['POST'])
def fetech_mutiple_document_by_actual_mode():
    actual_mode = request.form['actual_mode']
    amount = request.form['amount']
    """
    Function to retreive all 
    data based on a given actual model
    """
    try:
        if collection.count_documents({'actual_mode':actual_mode}) >0:
            # fetch customers by query parameters
            records_fetched = collection.find({'actual_mode':actual_mode}).limit(int(amount))
            user = eval(dumps(records_fetched))
            return render_template('query1.2.html', users=user)
        else:
            return 'No records are found', 404
    except Exception as e:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return e, 500


@app.route("/stat_show",methods = ['GET', 'POST'])
def stais_report():
    '''
    Function to show statistics info for certian customer

    '''
    try:
        result = db.command("dbstats")
        user = eval(dumps(result))
        return user
    except Exception as e:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return e, 500

@app.route('/insert', methods=['GET'])
def query6():
    return render_template('query6.html')

@app.route('/insert', methods=['POST'])
def insert_new_data():
    """
    Function to insert new document to the database
    """
    customer = request.form['customer']
    distance = request.form['distance']
    cases = request.form['cases']
    weight = request.form['weight']
    volume = request.form['volume']
    actual_carrier = request.form['actual_carrier']
    actual_mode = request.form['actual_mode']
    actual_equip = request.form['actual_equip']
    pu_appt = request.form['pu_appt']
    dl_appt = request.form['dl_appt']
    linehaul_costs = request.form['linehaul_costs']
    origin_lat = request.form['origin_lat']
    origin_lng = request.form['origin_lng']
    dest_lat = request.form['dest_lat']
    dest_lng = request.form['dest_lng']
    spot_avg_linehaul_rate = request.form['spot_avg_linehaul_rate']
    spot_low_linehaul_rate = request.form['spot_low_linehaul_rate']
    spot_high_linehaul_rate = request.form['spot_high_linehaul_rate']
    spot_fuel_surcharge = request.form['spot_fuel_surcharge']
    spot_time_frame = request.form['spot_time_frame']
    contract_avg_linehaul_rate = request.form['contract_avg_linehaul_rate']
    contract_low_linehaul_rate = request.form['contract_low_linehaul_rate']
    contract_high_linehaul_rate = request.form['contract_high_linehaul_rate']
    contract_fuel_surcharge = request.form['contract_fuel_surcharge']
    contract_avg_accessorial_excludes_fuel = request.form['contract_avg_accessorial_excludes_fuel']
    contract_time_frame = request.form['contract_time_frame']
    try:
        collection.insert_one({'customer':customer,'distance':distance,'cases':cases,'weight':weight,'volume':volume,'actual_carrier':actual_carrier,'actual_mode':actual_mode,'actual_equip':actual_equip,'pu_appt':pu_appt,'dl_appt':dl_appt, 'linehaul_costs':linehaul_costs, 'origin_lat':origin_lat, 'origin_lng':origin_lng, 'dest_lat':dest_lat, 'dest_lng':dest_lng, 'spot_avg_linehaul_rate':spot_avg_linehaul_rate,'spot_low_linehaul_rate':spot_low_linehaul_rate,'spot_high_linehaul_rate':spot_high_linehaul_rate,'spot_fuel_surcharge':spot_fuel_surcharge,'spot_time_frame':spot_time_frame,'contract_avg_linehaul_rate':contract_avg_linehaul_rate,'contract_low_linehaul_rate':contract_low_linehaul_rate,'contract_high_linehaul_rate':contract_high_linehaul_rate,'contract_fuel_surcharge':contract_fuel_surcharge,'contract_avg_accessorial_excludes_fuel':contract_avg_accessorial_excludes_fuel,'contract_time_frame':contract_time_frame})
        records_fetched = collection.find({'customer':customer,'distance':distance,'cases':cases,'weight':weight,'volume':volume,'actual_carrier':actual_carrier,'actual_mode':actual_mode,'actual_equip':actual_equip,'pu_appt':pu_appt,'dl_appt':dl_appt, 'linehaul_costs':linehaul_costs, 'origin_lat':origin_lat, 'origin_lng':origin_lng, 'dest_lat':dest_lat, 'dest_lng':dest_lng, 'spot_avg_linehaul_rate':spot_avg_linehaul_rate,'spot_low_linehaul_rate':spot_low_linehaul_rate,'spot_high_linehaul_rate':spot_high_linehaul_rate,'spot_fuel_surcharge':spot_fuel_surcharge,'spot_time_frame':spot_time_frame,'contract_avg_linehaul_rate':contract_avg_linehaul_rate,'contract_low_linehaul_rate':contract_low_linehaul_rate,'contract_high_linehaul_rate':contract_high_linehaul_rate,'contract_fuel_surcharge':contract_fuel_surcharge,'contract_avg_accessorial_excludes_fuel':contract_avg_accessorial_excludes_fuel,'contract_time_frame':contract_time_frame})
        user = eval(dumps(records_fetched))
        return render_template('query1.2.html', users=user)
    except Exception as e:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return e, 500

@app.route('/separate_dashboard', methods=['GET'])
def query7_dashboard():
    return render_template('query7_dashboard.html')

@app.route('/separate_dashboard/mt', methods=['GET'])
def return_mt():
    return render_template('query7_mt.html')

@app.route("/separate_dashboard/mt",methods = ['POST'])
def mt_data():
    """
    Function to retreive all 
    data in MT data
    """
    amount = request.form['amount']
    try:
        records_fetched = collection.find({}, {'customer':1,'distance':1,'cases':1,'weight':1,'volume':1,'actual_carrier':1,'actual_mode':1,'actual_equip':1,'pu_appt':1,'dl_appt':1}).limit(int(amount))
        user = eval(dumps(records_fetched))
        return render_template('query1.2.html', users=user)
    except Exception as e:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return e, 500
    
@app.route('/separate_dashboard/dat', methods=['GET'])
def return_dat():
    return render_template('query7_dat.html')

@app.route("/separate_dashboard/dat",methods = ['POST'])
def dat_data():
    """
    Function to retreive all 
    data in MT data
    """
    amount = request.form['amount']
    try:
        # fetch customers by query parameters
        records_fetched1 = collection.find({},{'spot_avg_linehaul_rate':1,'spot_low_linehaul_rate':1,'spot_high_linehaul_rate':1,'spot_fuel_surcharge':1,'spot_time_frame':1,'contract_avg_linehaul_rate':1,'contract_low_linehaul_rate':1,'contract_high_linehaul_rate':1,'contract_fuel_surcharge':1,'contract_avg_accessorial_excludes_fuel':1,'contract_time_frame':1}).limit(int(amount))
        user = eval(dumps(records_fetched1))
        return render_template('query1.2.html', users=user)
    except Exception as e:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return e, 500


if __name__ == '__main__':
    ''' 
        Running app in debug mode
        It will trace errors if produced and display them
        Each time a change is made in code, the changes will reflect instantaneously. 
    '''
    app.run(debug=True)