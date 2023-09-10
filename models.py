from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer,DateTime
import os

'''local database URL
database_name = "capstone"
#database_path = "postgresql://{}/{}".format('localhost:5432', database_name)'''

database_path = os.environ.get("DATABASE_PATH")
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
    with app.app_context(): #uncomment if FLASK version is 2.3 and above
        db.create_all()


class Movie(db.Model):
    '''This class represents the movies table'''
    __tablename__ = 'movies'

    id = Column(Integer,primary_key=True)
    title = Column(String(255),nullable=False)
    release_date = Column(DateTime,nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
            }
    
class Actor(db.Model):
    '''This class represents the actors table'''
    __tablename__ = 'actors'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),nullable=False)
    age = Column(Integer,default = 35)
    gender = Column(String(10),default = "None")

    def __init__(self,name,age,gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


