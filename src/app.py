"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from sqlalchemy import select
from models import db, User, Planets, People, Favoritos
#from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#LISTAR USUARIOS
@app.route('/user', methods=['GET'])
def handle_hello():
    try:
        data = db.session.scalars(select(User)).all()
        results = list(map(lambda item: item.serialize(), data))

        response_body = {
            "msg": "Hello, this is your GET /user response ",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error en /user: {e}")
        return jsonify({"error": "An error occurred"}), 500


#consulta de un solo registro
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = db.session.execute(select(User).filter_by(id=id)).scalar_one()

        response_body = {
            "msg": "Hello, this is your GET /user response ",
            "result":user.serialize()
        }

        return jsonify(response_body), 200
    except:
        return jsonify({"msg":"user not exist"}), 404

#listar todos los personajes (people)
@app.route('/people', methods=['GET'])
def handle_people():
    try:
        data = db.session.scalars(select(People)).all()
        results = list(map(lambda item: item.serialize(), data))

        response_body = {
            "msg": "Hello, this is your GET /people response ",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error en /people: {e}")
        return jsonify({"error": "An error occurred"}), 500
    
#listar personajes por id (people)
@app.route('/people/<int:id>', methods=['GET'])
def one_people(id):
    try:
        people = db.session.execute(select(People).filter_by(id=id)).scalar_one()

        response_body = {
            "msg": "Hello, this is your GET /people response ",
            "result":people.serialize()
        }

        return jsonify(response_body), 200
    except:
        return jsonify({"msg":"people not exist"}), 404
    
#listar todos los planetas (planets)
@app.route('/planets', methods=['GET'])
def handle_planets():
    try:
        data = db.session.scalars(select(Planets)).all()
        results = list(map(lambda item: item.serialize(), data))

        response_body = {
            "msg": "Hello, this is your GET /planets response ",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as e:
        print(f"Error en /people: {e}")
        return jsonify({"error": "An error occurred"}), 500
    
#listar planetas por id (planetas)
@app.route('/planets/<int:id>', methods=['GET'])
def one_planet(id):
    try:
        planet = db.session.execute(select(Planets).filter_by(id=id)).scalar_one()

        response_body = {
            "msg": "Hello, this is your GET /people response ",
            "result":planet.serialize()
        }

        return jsonify(response_body), 200
    except:
        return jsonify({"msg":"planet not exist"}), 404

#listar favoritos
@app.route('/users/favorites', methods=['GET'])
def handle_favoritos():
    data = db.session.scalars(select(Favoritos)).all()
    results = list(map(lambda item: item.serialize(), data))
    if results == []:
        results = "no favoritos"
    response_body = {
        "results": results
    }
    return jsonify(response_body), 200

##### POST ENDPOINT
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 2  
    planet = db.session.get(Planets, planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    
    favorito = Favoritos(usuario_id=user_id, planeta_id=planet_id)
    db.session.add(favorito)
    db.session.commit()
    return jsonify(favorito.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 2
    people = db.session.get(People, people_id)
    if not people:
        return jsonify({"msg": "Character not found"}), 404
    
    favorito = Favoritos(usuario_id=user_id, personaje_id=people_id)
    db.session.add(favorito)
    db.session.commit()
    return jsonify(favorito.serialize()), 201

# ##### DELETE ENDPOINT
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 2
    favorito = db.session.scalars(select(Favoritos).where(Favoritos.usuario_id == user_id, Favoritos.planeta_id == planet_id)).first()
    if not favorito:
        return jsonify({"msg": "Favorite planet not found"}), 404
    
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 2
    favorito = db.session.scalars(select(Favoritos).where(Favoritos.usuario_id == user_id, Favoritos.personaje_id == people_id)).first()
    if not favorito:
        return jsonify({"msg": "Favorite people not found"}), 404
    
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"msg": "Favorite people deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
