import json
import sqlite3
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

@app.route('/api/risks', methods=['GET', 'POST'])
def collection():
    if request.method == 'GET':
        return('RISKS PAGE')
        # pass #handle gets
    elif request.method == 'POST':
        data = request.form
        result = add_risk_type(data['type'], data['user'])
        return jsonify(result)


@app.route('/api/risks/<risk_id>', methods=['GET', 'POST'])
def resource(risk_id):
    if request.method == 'GET':
        pass #handle gets
    elif request.method == 'POST':
        pass #handle post


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