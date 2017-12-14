from app import db

class Risk(db.Model):
    """docstring for Property"""

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)

    def __init__(self, type):
        self.type = type
