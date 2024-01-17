from flask import Flask, jsonify, request, make_response #make http requests and responses
from flask_sqlalchemy import SQLAlchemy #ORM, create schema, users, make requests
from flask_cors import CORS #solve the CORS issue
from os import environ #read some environment variables

app = Flask(__name__)
CORS(app) #Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') #we will have DATABASE_URL variable in compose.yml
db = SQLAlchemy(app)

#define a model
class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {"id": self.id, "name": self.name, "email": self.email}
    
db.create_all()

#create test route
@app.route("/test", methods=['GET'])
def test():
    return jsonify({"message": "the server is running."})

@app.route("/api/flask/users", methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(name = data['name'], email = data['email']) #store python dictionary
        db.session.add(new_user) #creating a user
        db.session.commit() #commit these actions
    
        return jsonify({
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }), 201
    except Exception as e:
        return make_response(jsonify({"message": "error creating user", "error": str(e)}), 500) #don't make app crush, create an error exception
    
#get all users
@app.route("/api/flask/users", methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({'users': [user.json() for user in users]}), 200)
    except:
        return make_response(jsonify({"message": "error getting user"}), 500)

#get a user by id
@app.route("/users/<int:id>", methods=['GET'])
def get_user(id):
    try:
        users = User.query.all()
        return make_response(jsonify({'users': [user.json() for user in users]}), 200)
    except:
        return make_response(jsonify({"message": "error getting users"}), 500)
    
#update user
@app.route("/users/<int:id>", methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.name = data["name"]
            user.email = data["email"]
            db.session.commit()
            return make_response(jsonify({"message": "user updated"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except:
        return make_response(jsonify({"message": "error updating a user"}), 500)

    
#delete user
@app.route("/users/<int:id>", methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": "user deleted"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except:
        return make_response(jsonify({"message": "error deleting a user"}), 500)
