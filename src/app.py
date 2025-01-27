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

@app.route('/user', methods=['GET'])
def handle_hello():

    #consulta de todos los valores de una tabla
    data = db.session.scalars(select(User)).all()
    results = list(map(lambda item: item.serialize(),data))

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "results":results
    }

    return jsonify(response_body), 200


#consulta de un solo registro
# @app.route('/user/<int:id>', methods=['GET'])
# def get_user(id):
#     try:
#         user = db.session.execute(select(User).filter_by(id=id)).scalar_one()

#         response_body = {
#             "msg": "Hello, this is your GET /user response ",
#             "result":user.serialize()
#         }

#         return jsonify(response_body), 200
#     except:
#         return jsonify({"msg":"user not exist"}), 404


# ##### POST ENDPOINT
# @app.route('/user', methods=['POST'])
# def create_user():
#     request_data = request.json
#     print(request_data)
#     user = User(email=request_data["email"], password=request_data["password"])
#     db.session.add(user)
#     db.session.commit()

#     response_body = {
#         "msg":"user created"
#     }

#     return jsonify(response_body), 200

# ##### DELETE ENDPOINT
# @app.route('/user/<int:id>', methods=['DELETE'])
# def delete_user(id):

#     user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
#     db.session.delete(user)
#     db.session.commit()

#     response_body = {
#         "msg":"user deleted"
#     }

#     return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
