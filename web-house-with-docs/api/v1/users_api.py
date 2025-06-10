from data.__all_models import *
from flask import Blueprint, jsonify, request
from data import db_session

blueprint = Blueprint('users_api', __name__, template_folder='../templates')


@blueprint.route('/api/v1/users')
def get_users():
    session = db_session.create_session()
    users = session.query(Users).all()
    return jsonify({'users': [user.to_dict(only=('id', 'email', 'login', 'is_admin')) for user in users]})


@blueprint.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        return jsonify({'error': 'user not found'})
    return jsonify({'users': [user.to_dict(only=('id', 'email', 'login', 'is_admin'))]})


@blueprint.route('/api/v1/users', methods=['POST'])
def create_user():
    session = db_session.create_session()
    users = session.query(Users).all()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['login', 'password', 'email', 'is_admin']):
        return jsonify({'error': 'not enough arguments'})
    else:
        for user in users:
            if request.json['email'] == user.email:
                return jsonify({'error': 'user with this email already exists'})
            if request.json['login'] == user.login:
                return jsonify({'error': 'user with this login already exists'})

    user = Users(
        login=request.json['login'],
        email=request.json['email'],
        is_admin=request.json['is_admin']
    )
    user.set_password(request.json['password'])
    session.add(user)
    session.commit()
    return jsonify({'success': 'user added'})


@blueprint.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        return jsonify({'error': 'user not found'})
    posts = user.posts
    if posts:
        for post in posts:
            session.delete(post)
    session.delete(user)
    session.commit()
    return jsonify({'success': 'user deleted'})


@blueprint.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['login', 'email', 'is_admin']):
        return jsonify({'error': 'not enough arguments'})
    user = session.query(Users).get(user_id)
    if not user:
        return jsonify({'error': 'user not found'})
    user.login = request.json['login']
    user.email = request.json['email']
    user.is_admin = request.json['is_admin']
    session.commit()
    return jsonify({'success': 'user edited'})


@blueprint.route('/api/v1/users/<int:user_id>/reviews')
def get_posts(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        return jsonify({'error': 'user not found'})
    posts = user.posts
    return jsonify({'reviews': [post.to_dict(only=('id', 'user_id', 'body', 'categories')) for post in posts]})
