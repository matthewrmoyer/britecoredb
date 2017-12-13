from app import db, models
from models import Risk


db.session.query(models.Risk).delete()
db.session.commit()

risk1 = Risk('Scholarship')


#   '\xe7\xe9' add this to property

db.session.add(risk1)
db.session.commit()
