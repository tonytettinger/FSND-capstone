import os
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "antaltettinger"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
class Movie(db.Model):  
  __tablename__ = 'Movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date
    
  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date}
    
class Actor(db.Model):  
  __tablename__ = 'Actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender
    
  def format(self):
    return {
      'id': self.name,
      'title': self.age,
      'release_date': self.gender}
    