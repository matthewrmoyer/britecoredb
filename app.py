import json
import sqlite3
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

@app.route('/api/risks', methods=['GET', 'POST'])
def risk_collection():
    if request.method == 'GET':
        all_risks_types = get_all_risk_types()
        return json.dumps(all_risks_types)
        # pass #handle gets
    elif request.method == 'POST':
        data = request.form
        result = add_risk_type(data['type'], data['user'])
        return jsonify(result)


@app.route('/api/risks/<risk_id>', methods=['GET', 'POST'])
def resource(risk_id):
    if request.method == 'GET':
        risk_type = get_risk_type_by_id(risk_id)
        return json.dumps(risk_type)
    elif request.method == 'POST':
        pass #handle post


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


if __name__ == '__main__':
    app.debug = True
    app.run()

    # curl --data "type='Scholarship'&user='matthewrmoyer@gmail.com'"  http://localhost:5000/api/risks