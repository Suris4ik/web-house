from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.__all_models import *
from api.v2.parser import ParserUsers

parser = ParserUsers()


def users_not_found(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')


class UsersResource(Resource):
    def get(self, user_id):
        users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        return jsonify({'users': user.to_dict(only=('id', 'login', 'is_admin', 'email'))})

    def delete(self, user_id):
        users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        posts = user.posts
        if posts:
            for post in posts:
                session.delete(post)
        session.delete(user)
        session.commit()
        return jsonify({'success': f'User {user_id} was deleted'})

    def put(self, user_id):
        args = parser.parse_args()
        users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        if 'login' in args:
            user.login = args['login']
        if 'email' in args:
            user.email = args['email']
        if 'password' in args:
            user.set_password(args['password'])
        if 'is_admin' in args:
            if args['is_admin'] == 'true':
                user.is_admin = True
            else:
                user.is_admin = False
        session.commit()
        return jsonify({'success': 'user edited'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(Users).all()
        return jsonify({'users': [user.to_dict(only=('id', 'login', 'is_admin', 'email')) for user in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if not all(key in args for key in ['email', 'login', 'password']):
            return jsonify({'error': 'not enough arguments'})
        user = Users(
            email=args['email'],
            login=args['login']
        )
        if 'is_admin' in args:
            if args['is_admin'] == 'true':
                user.is_admin = True
            else:
                user.is_admin = False
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'user added'})
