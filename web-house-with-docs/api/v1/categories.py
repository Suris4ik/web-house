from flask import Blueprint, jsonify, request

from data import db_session
from data.__all_models import *

blueprint = Blueprint('categories_api', __name__, template_folder='../templates')


@blueprint.route('/api/v1/categories')
def get_all_categories():
    session = db_session.create_session()
    categories = session.query(Categories).all()
    return jsonify({'categories': [category.to_dict(only=('id', 'name')) for category in categories]})


@blueprint.route('/api/v1/categories/<int:category_id>', methods=['GET'])
def get_one_category(category_id):
    session = db_session.create_session()
    category = session.query(Categories).get(category_id)
    if not category:
        return jsonify({'error': 'category not found'})
    return jsonify({'categories': category.to_dict(only=('id', 'name'))})


@blueprint.route('/api/v1/categories', methods=['POST'])
def create_category():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif 'name' not in request.json:
        return jsonify({'error': 'missing name in request'})
    category = Categories(name=request.json['name'])
    session.add(category)
    session.commit()
    return jsonify({'success': 'category added'})


@blueprint.route('/api/v1/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    session = db_session.create_session()
    category = session.query(Categories).get(category_id)
    posts = category.posts
    if posts:
        for post in posts:
            session.delete(post)
    session.delete(category)
    session.commit()
    return jsonify({'success': 'category deleted'})


@blueprint.route('/api/v1/categories/<int:category_id>', methods=['PUT'])
def edit_category(category_id):
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif 'name' not in request.json:
        return jsonify({'error': 'missing name argument'})
    category = session.query(Categories).get(category_id)
    if not category:
        return jsonify({'error': 'category not found'})
    category.name = request.json['name']
    session.commit()
    return jsonify({'success': 'category edited'})


@blueprint.route('/api/v1/categories/<int:category_id>/posts')
def get_posts(category_id):
    session = db_session.create_session()
    category = session.query(Categories).get(category_id)
    if not category:
        return jsonify({'error': 'category not found'})
    posts = category.posts
    return jsonify({'posts': [post.to_dict(only=('id', 'user_id', 'body')) for post in posts]})