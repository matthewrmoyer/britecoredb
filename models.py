from app import db


class Property(db.Model):
    """docstring for Property"""

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)
    temperature = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    image = db.Column(db.String)
    # imageb = db.Column(db.LargeBinary)

    def __init__(self, location, temperature, image):
        self.location = location
        self.temperature = temperature
        self.image = image
        # self.imageb = imageb
        # will have to fix this
