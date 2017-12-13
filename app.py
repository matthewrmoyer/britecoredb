import sqlite3
from flask import Flask, request

app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run()

@app.route('/api/risks', methods=['GET', 'POST'])
def risks():
    if request.method == 'GET':
        pass #handle gets
    elif request.method == 'POST':
        pass #handle post


@app.route('/api/risks/<risk_id>', methods=['GET', 'POST'])
def risks():
    if request.method == 'GET':
        pass #handle gets
    elif request.method == 'POST':
        pass #handle post


if __name__ == '__main__':
    app.debug = True
    app.run()