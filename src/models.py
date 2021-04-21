from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    mail = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.mail,
            # do not serialize the password, its a security breach
        }

class Personajes(db.Model):
    __tablename__ = 'personajes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            # do not serialize the password, its a security breach
        }

class Planetas(db.Model):
    __tablename__ = 'planetas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "population": self.population,
            "terrain": self.terrain,
            # do not serialize the password, its a security breach
        }


class Favoritos(db.Model):
    __tablename__ = 'favoritos'

    id = db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tipoFavorito = db.Column(db.String(250), nullable=False)
    favoritoId = db.Column(db.String(250), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "User_id": self.User_id,
            "tipoFavorito": self.tipoFavorito,
            "favoritoId": self.favoritoId,
            # do not serialize the password, its a security breach
        }

