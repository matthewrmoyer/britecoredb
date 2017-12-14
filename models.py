from app import db

class Risk(db.Model):
    """docstring for Property"""

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)

    # def __init__(self, type):
    #     self.type = type


class Field(db.Model):
    """docstring for Property"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)    
    risk_type = db.Column(db.String)
    data_type = db.Column(db.String)
    
    # def __init__(self, name, risk_type, data_type):
    #     self.name = name
    #     self.risk_type = risk_type
    #     self.data_type = data_type