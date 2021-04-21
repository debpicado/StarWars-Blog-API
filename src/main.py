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
from models import db, User, Planetas, Personajes
#from models import Person

#import JWT for tokenization
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# config for jwt
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

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

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/register', methods=['POST'])
def register_user():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # valida si estan vacios los ingresos
    if email is None:
        return jsonify({"msg": "No email was provided"}), 400
    if password is None:
        return jsonify({"msg": "No password was provided"}), 400
    
    # busca usuario en BBDD
    user = User.query.filter_by(email=email).first()
    if user:
        # the user was not found on the database
        return jsonify({"msg": "User already exists"}), 401
    else:
        # crea usuario nuevo
        # crea registro nuevo en BBDD de 
        return jsonify({"msg": "User created successfully"}), 200

@app.route('/login', methods=['POST']) 
def login():
    user = request.json.get("email", None)
    password = request.json.get("password", None)

    # valida si estan vacios los ingresos
    if user is None:
        return jsonify({"msg": "No email was provided"}), 400
    if password is None:
        return jsonify({"msg": "No password was provided"}), 400

    # para proteger contraseñas usen hashed_password
    # busca usuario en BBDD
    user = User.query.filter_by(user=user, password=password).first()
    if user is None:
        return jsonify({"msg": "Invalid username or password"}), 401
    else:
        # crear token
        my_token = create_access_token(identity=user.id)
        return jsonify({"token": my_token})

@app.route('/personajes', methods=['GET']) 
def personajes():
    name = request.json.get("name", None)
    gender = request.json.get("gender", None)
    hair_color = request.json.get("hair_color", None)
    eye_color = request.json.get("eye_color", None)

    if name is None:
        return jsonify({"msg": "No Name was provided"}), 400
    if gender is None:
        return jsonify({"msg": "No gender was provided"}), 400
    if hair_color is None:
        return jsonify({"msg": "No hair_color was provided"}), 400
    if eye_color is None:
        return jsonify({"msg": "No eye_color was provided"}), 400

    personajes = Personajes.query.filter_by(name=name, gender=gender,hair_color=hair_color,eye_color=eye_color).first()

    if personajes:
        # the user was not found on the database
        return jsonify({"msg": "personajes already exists"}), 401
    else:
        # crea usuario nuevo
        # crea registro nuevo en BBDD de
        personajes = Personajes(name=name, gender=gender, hair_color=hair_color,eye_color=eye_color)
        db.session.add(personajes)
        db.session.commit()
        return jsonify({"msg": "personajes created successfully"}), 200

@app.route('/planetas', methods=['GET']) 
def planetas():
    name = request.json.get("name", None)
    diameter = request.json.get("diameter", None)
    population = request.json.get("population", None)
    terrain = request.json.get("terrain", None)

    if name is None:
        return jsonify({"msg": "No Name was provided"}), 400
    if diameter is None:
        return jsonify({"msg": "No diameter was provided"}), 400
    if population is None:
        return jsonify({"msg": "No population was provided"}), 400
    if terrain is None:
        return jsonify({"msg": "No terrain was provided"}), 400

    planetas = Planetas.query.filter_by(name=name, diameter=diameter,population=population,terrain=terrain).first()
    
    if planetas:
        # the user was not found on the database
        return jsonify({"msg": "planetas already exists"}), 401
    else:
        # crea usuario nuevo
        # crea registro nuevo en BBDD de
        planetas = Planetas(name=name, diameter=diameter, population=population,terrain=terrain)
        db.session.add(planetas)
        db.session.commit()
        return jsonify({"msg": "planetas created successfully"}), 200

@app.route('/favoritos', methods=['GET']) 
def favoritos():
    User_id = request.json.get("User_id", None)
    tipoFavorito = request.json.get("tipoFavorito", None)
    favoritoId = request.json.get("favoritoId", None)

    favoritos = Favoritos.query.filter_by(User_id=User_id, tipoFavorito=tipoFavorito,favoritoId=favoritoId).first()


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
