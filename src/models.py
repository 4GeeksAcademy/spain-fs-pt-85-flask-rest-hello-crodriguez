from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import mapped_column
# from sqlalchemy import Integer, String, Boolean
# from sqlalchemy.orm import declarative_base
# from sqlalchemy import create_engine
# # # from eralchemy2 import render_er
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(20), unique=True, nullable=False)
    fecha_suscripcion = db.Column(db.String(20), unique=True, nullable=False)
    favoritos = db.Column(db.Integer, db.ForeignKey('favoritos.id'))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "fecha_suscripcion": self.fecha_suscripcion,
            "favoritos": self.favoritos
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = "planets"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    sistema = db.Column(db.String(50), unique=True, nullable=False)
    favoritos = db.relationship("Favoritos")

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "sistema": self.sistema,
            "favoritos": self.favoritos
        }

class People(db.Model):
    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    especie = db.Column(db.String(50), unique=True, nullable=False)
    favoritos = db.relationship("Favoritos")

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "favoritos": self.favoritos
        }

class Favoritos(db.Model):
    __tablename__ = 'favoritos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planeta_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    personaje_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    

    # def serialize(self):
    #     return{
    #         "id": self.id,
    #         "usuario_id": self.usuario_id,
    #         "planeta_id": self.planeta_id,
    #         "personaje_id": self.personaje_id
    #     }


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