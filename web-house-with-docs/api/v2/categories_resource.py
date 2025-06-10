from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.__all_models import *
from api.v2.parser import ParserCategories

parser = ParserCategories()


def categories_not_found(category_id):
    session = db_session.create_session()
    category = session.query(Categories).get(category_id)
    if not category:
        abort(404, message=f'Category {category_id} not found')


class CategoriesResource(Resource):
    def get(self, category_id):
        categories_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Categories).get(category_id)
        return jsonify({'categories': category.to_dict(only=('id', 'name'))})

    def delete(self, category_id):
        categories_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Categories).get(category_id)
        session.delete(category)
        session.commit()
        return jsonify({'success': f'Category {category_id} deleted'})

    def put(self, category_id):
        args = parser.parse_args()
        categories_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Categories).get(category_id)
        if 'name' in args:
            category.name = args['name']
        session.commit()
        return jsonify({'success': 'category edited'})


class CategoriesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        categories = session.query(Categories).all()
        return jsonify({'categories': [category.to_dict(only=('id', 'name')) for category in categories]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if 'name' not in args:
            return jsonify({'error': 'missing name argument'})
        category = Categories(name=args['name'])
        session.add(category)
        session.commit()
        return jsonify({'success': 'category added'})

class CategoryPosts(Resource):
    def get(self, category_id):
        categories_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Categories).get(category_id)
        posts = category.posts
        posts_ = []
        for post in posts:
            categories = [category.name for category in post.categories]
            post = post.to_dict(only=('id', 'user_id', 'body'))
            user = session.query(Users).get(post['user_id'])
            post['categories'] = categories
            post['user'] = user.login
            posts_.append(post)
        return jsonify({'posts': posts_})