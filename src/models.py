from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Boolean, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
# from eralchemy2 import render_er
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship




db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    favoritos = relationship("Favoritos", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email, 
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = "planets"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50),  nullable=False)
    sistema = Column(String(50), nullable=False)
    favoritos = relationship("Favoritos", back_populates="planets")

    def __repr__(self):
        return f'<Planets {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "sistema": self.sistema
        }

class People(db.Model):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    especie = Column(String(50), nullable=False)
    favoritos = relationship("Favoritos", back_populates="people")

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
        }

class Favoritos(db.Model):
    __tablename__ = 'favoritos'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('user.id'))
    planeta_id = Column(Integer, ForeignKey('planets.id'))
    personaje_id = Column(Integer, ForeignKey('people.id'))
    user = relationship("User", back_populates="favoritos")
    planets = relationship("Planets", back_populates="favoritos")
    people = relationship("People", back_populates="favoritos")
    

    def serialize(self):
        return{
            "id": self.id,
            "usuario_id": self.usuario_id,
            "planeta_id": self.planeta_id,
            "personaje_id": self.personaje_id
        }


# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }