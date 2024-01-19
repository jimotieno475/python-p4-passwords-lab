#!/usr/bin/env python3

from flask import request, session,abort
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username'],
            password_hash=json['password']
        )
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get (self):
        user_id=session['user_id']
        if user_id:
            user=User.query.filter(User.id== user_id).first()
            return user.to_dict(),200
        return{},204

# class CheckSession(Resource):
#     def get(self):
#         user_id = session.get('user_id')

#         if user_id:
#             user = User.query.filter(User.id == user_id).first()
            
#             if user:
#                 return user.to_dict(), 200
#             else:
#                 # Handle the case where the user is not found (optional)
#                 abort(404, message="User not found")
#         else:
#             # User is not authenticated, return an empty response with a 204 status code
#             return {},
#     pass

class Login(Resource):

    def post(self):

        username = request.get_json()['username']
        user = User.query.filter(User.username == username)

        _password_hash = request.get_json()['password']
        if _password_hash == user._password_hash:
            session['user_id'] = user.id
            return user.to_dict(), 200

        return {'error': 'Invalid username or password'}, 401

class Logout(Resource):
    def delete(self):
        session['user_id']=None
        return {},204
    pass

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession,'/check_session',endpoint='check_session')
api.add_resource(Login,'/login' , endpoint='login')
api.add_resource(Logout,'/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
