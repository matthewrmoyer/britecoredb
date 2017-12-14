from flask import Flask, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json
import os


print('app.py working')
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost:5432/britecore_db'
# UPLOAD_FOLDER = './fileuploadfolder'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
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





@app.route('/risk', methods=['GET'])
def risks():
    if request.method == 'GET':
        all_risks = []
        risks = models.Risk.query.all()
        for risk in risks:
            all_risks.append({
                'id': risk.id,
                'type': risk.type,
            })
        return jsonify(all_risks)








@app.route('/environment', methods=['GET', 'POST'])
def environment():
    if request.method == 'GET':
        all_environment_data = []
        properties = models.Property.query.all()
        for property in properties:
            all_environment_data.append({
                'id': property.id,
                'location': property.location,
                'temperature': property.temperature,
                'timestamp': property.timestamp,
                'image': property.image
                # 'imageb': property.imageb
            })
        return jsonify(all_environment_data)
    elif request.method == 'POST':
        new_property_data = json.loads(request.data)
        new_property = models.Property(
            new_property_data["location"], new_property_data[
                "temperature"], new_property_data["image"]
            # new_property_data["imageb"]
        )
        db.session.add(new_property)
        db.session.commit()
        return request.data


@app.route('/temperature', methods=['GET', 'POST'])
def temperature():
    return "Temperature Data"


@app.route('/lighting', methods=['GET', 'POST'])
def lighting():
    return "Lighting Data"


@app.route('/images', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return 'HASFDASF'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'uploaded?'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=port)