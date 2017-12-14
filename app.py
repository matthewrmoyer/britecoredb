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

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost:5432/britecore_db'
# UPLOAD_FOLDER = './fileuploadfolder'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# engine = create_engine('postgres://localhost:5432/envirorpi_db')

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
        for new_field in new_fields_data:
            new_field = models.Field(
                new_fields_data["type"],
                new_fields_data["field"]["name"],                                
                new_fields_data["field"]["type"],                
        )
        db.session.add(new_risk)
        db.session.commit()
        return request.data
    # elif request.method == 'POST':
    #     new_risk_data = json.loads(request.data)
    #     new_risk = models.Risk(
    #         new_property_data["type"],
    #     )
    #     db.session.add(new_risk)
    #     db.session.commit()
    #     return request.data


# @app.route('/api/fields', methods=['GET', 'POST'])
# def risk__field_collection():
#     if request.method == 'GET':
#         all_risks_fields = get_all_risk_fields()
#         return json.dumps(all_risks_fields)
#     elif request.method == 'POST':
#         data = request.form
#         result = add_risk_field(data['name'], data['risk_type'], data['data_type'])
#         return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=port)




# @app.route('/api/risks', methods=['GET', 'POST'])
# def risk__type_collection():
#     if request.method == 'GET':
#         all_risks_types = get_all_risk_types()
#         return json.dumps(all_risks_types)
#         # ADD IN THE RISK FIELDS 
#     elif request.method == 'POST':
#         data = request.form
#         result = add_risk_type(data['type'], data['user'])
#         return jsonify(result)


# @app.route('/api/fields', methods=['GET', 'POST'])
# def risk__field_collection():
#     if request.method == 'GET':
#         all_risks_fields = get_all_risk_fields()
#         return json.dumps(all_risks_fields)
#     elif request.method == 'POST':
#         data = request.form
#         result = add_risk_field(data['name'], data['risk_type'], data['data_type'])
#         return jsonify(result)


# @app.route('/api/fields/<risk_type>', methods=['GET'])
# def field_resource(risk_type):
#     if request.method == 'GET':
#         fields = get_risk_fields_by_risk_type(risk_type)
#         # ADD IN THE RISK FIELDS         
#         return json.dumps(fields)


# @app.route('/api/risks/<risk_id>', methods=['GET'])
# def risk_resource(risk_id):
#     if request.method == 'GET':
#         risk_type = get_risk_type_by_id(risk_id)
#         # ADD IN THE RISK FIELDS         
#         return json.dumps(risk_type)


# def get_all_risk_types():
#     with sqlite3.connect('risks.db') as connection:
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM risk_types ORDER BY id desc")
#         all_risk_types = cursor.fetchall()
#         return all_risk_types


# def get_risk_type_by_id(risk_type_id):
#     with sqlite3.connect('risks.db') as connection:
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM risk_types WHERE id = ?", (risk_type_id))
#         risk_type = cursor.fetchone()
#         return risk_type


# def add_risk_type(type, user):
#     try:
#         with sqlite3.connect('risks.db') as connection:
#             cursor = connection.cursor()
#             cursor.execute("""
#                 INSERT INTO risk_types (type, user) values (?, ?);
#                 """, (type, user))
#             result = {'status': 1, 'message': 'Risk Type Added'}
#     except Exception as e:
#         logging.exception("message")
#     return result


# def get_all_risk_fields():
#     with sqlite3.connect('risks.db') as connection:
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM risk_fields ORDER BY id desc")
#         all_risk_fields = cursor.fetchall()
#         return all_risk_fields


# def get_risk_fields_by_risk_type(risk_type):
#     with sqlite3.connect('risks.db') as connection:
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM risk_fields WHERE risk_type LIKE ?", [risk_type])
#         risk_fields = cursor.fetchall()
#         return risk_fields
        

# def add_risk_field(name, risk_type, data_type):
#     try:
#         with sqlite3.connect('risks.db') as connection:
#             cursor = connection.cursor()
#             cursor.execute("""
#                 INSERT INTO risk_fields (name, risk_type, data_type) values (?, ?, ?);
#                 """, (name, risk_type, data_type))
#             result = {'status': 1, 'message': 'Risk Field Added'}
#     except Exception as e:
#         logging.exception("message")
#     return result


    # @app.route('/environment', methods=['GET', 'POST'])
# def environment():
#     if request.method == 'GET':
#         all_environment_data = []
#         properties = models.Property.query.all()
#         for property in properties:
#             all_environment_data.append({
#                 'id': property.id,
#                 'location': property.location,
#                 'temperature': property.temperature,
#                 'timestamp': property.timestamp,
#                 'image': property.image
#                 # 'imageb': property.imageb
#             })
#         return jsonify(all_environment_data)
#     elif request.method == 'POST':
#         new_property_data = json.loads(request.data)
#         new_property = models.Property(
#             new_property_data["location"], new_property_data[
#                 "temperature"], new_property_data["image"]
#             # new_property_data["imageb"]
#         )
#         db.session.add(new_property)
#         db.session.commit()
#         return request.data