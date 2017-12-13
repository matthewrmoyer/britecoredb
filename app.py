import json
import sqlite3
from flask import Flask, request, jsonify
import logging


app = Flask(__name__)

@app.route('/api/risks', methods=['GET', 'POST'])
def risk__type_collection():
    if request.method == 'GET':
        all_risks_types = get_all_risk_types()
        return json.dumps(all_risks_types)
        # ADD IN THE RISK FIELDS 
    elif request.method == 'POST':
        data = request.form
        result = add_risk_type(data['type'], data['user'])
        return jsonify(result)


@app.route('/api/fields', methods=['GET', 'POST'])
def risk__field_collection():
    if request.method == 'GET':
        all_risks_fields = get_all_risk_fields()
        return json.dumps(all_risks_fields)
    elif request.method == 'POST':
        data = request.form
        result = add_risk_field(data['name'], data['risk_type'], data['data_type'])
        return jsonify(result)


@app.route('/api/fields/<risk_type>', methods=['GET'])
def field_resource(risk_type):
    if request.method == 'GET':
        fields = get_risk_fields_by_risk_type(risk_type)
        # ADD IN THE RISK FIELDS         
        return json.dumps(fields)


@app.route('/api/risks/<risk_id>', methods=['GET'])
def risk_resource(risk_id):
    if request.method == 'GET':
        risk_type = get_risk_type_by_id(risk_id)
        # ADD IN THE RISK FIELDS         
        return json.dumps(risk_type)


def get_all_risk_types():
    with sqlite3.connect('risks.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM risk_types ORDER BY id desc")
        all_risk_types = cursor.fetchall()
        return all_risk_types


def get_risk_type_by_id(risk_type_id):
    with sqlite3.connect('risks.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM risk_types WHERE id = ?", (risk_type_id))
        risk_type = cursor.fetchone()
        return risk_type


def add_risk_type(type, user):
    try:
        with sqlite3.connect('risks.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO risk_types (type, user) values (?, ?);
                """, (type, user))
            result = {'status': 1, 'message': 'Risk Type Added'}
    except Exception as e:
        logging.exception("message")
    return result


def get_all_risk_fields():
    with sqlite3.connect('risks.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM risk_fields ORDER BY id desc")
        all_risk_fields = cursor.fetchall()
        return all_risk_fields


def get_risk_fields_by_risk_type(risk_type):
    with sqlite3.connect('risks.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM risk_fields WHERE risk_type LIKE ?", [risk_type])
        risk_fields = cursor.fetchall()
        return risk_fields
        

def add_risk_field(name, risk_type, data_type):
    try:
        with sqlite3.connect('risks.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO risk_fields (name, risk_type, data_type) values (?, ?, ?);
                """, (name, risk_type, data_type))
            result = {'status': 1, 'message': 'Risk Field Added'}
    except Exception as e:
        logging.exception("message")
    return result


if __name__ == '__main__':
    app.debug = True
    app.run()

    # curl --data "type=Scholarship&user=matthewrmoyer@gmail.com"  http://localhost:5000/api/risks
    # curl --data "name=GPA&risk_type=Scholarship&data_type=text"  http://localhost:5000/api/fields
    # curl --data "name=Age&risk_type=Scholarship&data_type=number"  http://localhost:5000/api/fields