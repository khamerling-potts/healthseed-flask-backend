import json

# Remote library imports
from flask import request, session, make_response
from flask_restful import Resource

# Local imports
from config import app, db, api

# Model imports
from models.user import User
from models.condition import Condition



class Login(Resource):
    def post(self):
        data = request.get_json()
        [username, password] = [data.get('username'), data.get('password')]
        user = User.query.filter_by(username=username.lower()).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'error': '401 - Unauthorized'}, 401

class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return users, 200
    
    def post(self):
        data = request.get_json()
        [username, password, name, birthday] = [data.get('username'), data.get('password'), data.get('name'), data.get('birthday')]
        try:
            new_user = User(username=username, name=name, birthday=birthday)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_dict(), 200
        except Exception as exc:
            return {'error': '422 - Unprocessable Entity'}, 422


api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Users, "/users", endpoint="users")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
