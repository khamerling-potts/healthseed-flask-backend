import json

# Remote library imports
from flask import request, session, make_response
from flask_restful import Resource

# Local imports
from config import app, db, api


users = [
 { 'id': 1, 'name': 'Ashley' },
 { 'id': 2, 'name': 'Kate' },
 { 'id': 3, 'name': 'Joe' }
]


class Users(Resource):
    def get(self):
        return users, 200

api.add_resource(Users, "/users", endpoint="users")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
