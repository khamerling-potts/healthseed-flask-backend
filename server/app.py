import json

# Remote library imports
from flask import request, session, make_response
from flask_restful import Resource

# Local imports
from config import app, db, api

# Model imports
from models.user import User
from models.condition import Condition
from models.provider import Provider


@app.before_request
def check_logged_in():
    if request.endpoint not in ['login', 'users']:
        print('checking logged in')
        if not session.get('user_id'):
            return {'error': 'Unauthorized'}, 401
        
class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        return user.to_dict(), 200


class Login(Resource):
    def post(self):
        data = request.get_json()
        [username, password] = [data.get('username'), data.get('password')]
        user = User.query.filter_by(username=username.lower()).first()
        
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'error': '401 - Unauthorized'}, 401
    
class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204


class Users(Resource):
    def get(self):
        breakpoint()
        users = [user.to_dict() for user in User.query.all()]
        return users, 200
    
    def post(self):
        data = request.get_json()
        [username, password, name, birthday] = [data.get('username'), data.get('password'), data.get('name'), data.get('birthday')]
        try:
            new_user = User(username=username, name=name, birthday=birthday)
            print('1')
            new_user.password_hash = password
            print('2')
            db.session.add(new_user)
            print('3')
            db.session.commit()
            print('4')
            session['user_id'] = new_user.id
            print('5')
            return new_user.to_dict(), 200
        except Exception as exc:
            print(exc)
            return {'error': '422 - Unprocessable Entity'}, 422
        

class Conditions(Resource):
    def get(self):
        user_id = session.get('user_id')
        conditions = [condition.to_dict() for condition in Condition.query.filter_by(user_id=user_id)]
        return conditions, 200
    
    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()
        description = data.get('description')
        try:
            new_condition = Condition(description=description, user_id=user_id)
            print(new_condition)
            db.session.add(new_condition)
            db.session.commit()
            print('here')
            return new_condition.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': "422 - Unprocessable Entity"}, 422



api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Users, "/users", endpoint="users")
api.add_resource(Conditions, '/conditions', endpoint='conditions')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
