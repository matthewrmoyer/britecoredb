from app import db, models
from models import Risk
from models import Field



db.session.query(models.Risk).delete()
db.session.query(models.Field).delete()

db.session.commit()

risk1 = Risk('Scholarship')

field1 = Field('GPA', 'Scholarship', 'number')


db.session.add(risk1)
db.session.add(field1)

db.session.commit()
