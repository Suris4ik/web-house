from data import db_session
from data.__all_models import *
from flask import Blueprint, jsonify, request

blueprint = Blueprint('posts_api', __name__, template_folder='../templates')


@blueprint.route('/api/v1/posts', methods=['GET'])
def get_all_posts():
    session = db_session.create_session()
    posts = session.query(Posts).all()
    posts_ = []
    for post in posts:
        categories = [category.name for category in post.categories]
        post = post.to_dict(only=('id', 'user_id', 'body'))
        user = session.query(Users).get(post['user_id'])
        post['categories'] = categories
        post['user'] = user.login
        posts_.append(post)
    return jsonify(
        {'posts': posts_})

@blueprint.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def get_one_post(post_id):
    session = db_session.create_session()
    post = session.query(Posts).get(post_id)
    if not post:
        return jsonify({'error': 'post not found'})
    categories = [category.name for category in post.categories]
    post = post.to_dict(only=('id', 'user_id', 'body'))
    user = session.query(Users).get(post['user_id'])
    post['categories'] = categories
    post['user'] = user.login
    return jsonify({'posts': post})


@blueprint.route('/api/v1/posts', methods=['POST'])
def create_post():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['user_id', 'body']):
        return jsonify({'error': 'not enough arguments'})
    post = Posts(
        user_id=request.json['user_id'],
        body=request.json['body']
    )
    if 'categories' in request.json:
        for cat_id in request.json['categories']:
            if str(cat_id).isdigit():
                post.categories.append(session.query(Categories).get(int(cat_id)))
    session.add(post)
    session.commit()
    return jsonify({'success': 'post added'})


@blueprint.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    session = db_session.create_session()
    post = session.query(Posts).get(post_id)
    if not post:
        return jsonify({'error': 'post not found'})
    session.delete(post)
    session.commit()
    return jsonify({'success': 'post deleted'})


@blueprint.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
def edit_post(post_id):
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    post = session.query(Posts).get(post_id)
    if 'user_id' in request.json:
        post.user_id = request.json['user_id']
    if 'body' in request.json:
        post.body = request.json['body']
    if 'categories' in request.json:
        for cat_id in request.json['categories']:
            if str(cat_id).isdigit():
                post.categories.append(session.query(Categories).get(int(cat_id)))
    session.commit()
    return jsonify({'success': 'post edited'})