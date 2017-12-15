from flask import Flask, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json
import os
import psycopg2
from flask_cors import CORS, cross_origin



print('app.py working')
app = Flask(__name__)
CORS(app, resources=r'/*', headers='Content-Type')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

port = int(os.environ.get('PORT', 5000))
import models

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    print('hitting index route')
    return "Hello World"


@app.route('/risks', methods=['GET', 'POST'])
def risks_collection():
    if request.method == 'GET':
        all_risks = []
        risks = models.Risk.query.all()
        for risk in risks:
            all_risks.append({
                'id': risk.id,
                'type': risk.type,
            })
        return jsonify(all_risks)
    elif request.method == 'POST':
        new_risk_data = json.loads(request.data)
        new_risk = models.Risk(
            new_risk_data["type"],
        )
        db.session.add(new_risk)
        db.session.commit()
        return request.data


@app.route('/fields', methods=['GET', 'POST'])
def fields_collection():
    if request.method == 'GET':
        all_fields = []
        fields = models.Field.query.all()
        for field in fields:
            all_fields.append({
                'id': field.id,
                'name': field.name,
                'risk_type': field.risk_type,
                'data_type': field.data_type
            })
        return jsonify(all_fields)
    elif request.method == 'POST':
        new_fields_data = json.loads(request.data)
        for new_field in new_fields_data["fields"]:
            new_field = models.Field(
                new_field["name"],                                
                new_fields_data["type"],
                new_field["type"]    
            )
            db.session.add(new_field)
            db.session.commit()
        return request.data


@app.route('/risks/<risk_id>', methods=['GET'])
def risk_resource(risk_id):
    if request.method == 'GET':
        data = []
        risk = models.Risk.query.filter_by(id=risk_id).first()
        fields = models.Field.query.filter_by(risk_type=risk.type).all()
        data.append({
            'risk': {
            'id': risk.id,
            'type': risk.type,
            }
        })

        fieldArray = []
        for field in fields:
            fieldArray.append({
                'id': field.id,
                'name': field.name,
                'data_type': field.data_type
            })
        data.append({'fields': fieldArray})
        return jsonify(data)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=port)


