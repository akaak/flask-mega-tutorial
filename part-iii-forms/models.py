# models.py

from flask_sqlalchemy import SQLAlchemy
#from app import db
import datetime

db = SQLAlchemy()

class Bizs(db.Model):

    #__tablename__ = "bizs"

    biz_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)    
    added_date = db.Column(db.DATE, nullable=False)

    def __init__(self,name,description, added_date):
        self.name = name
        self.description = description
        self.added_date = added_date
        