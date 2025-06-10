from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.__all_models import *
from api.v2.parser import ParserPosts

parser = ParserPosts()


def posts_not_found(post_id):
    session = db_session.create_session()
    post = session.query(Posts).get(post_id)
    if not post:
        abort(404, message=f'Post {post_id} not found')


class PostsResource(Resource):
    def get(self, post_id):
        posts_not_found(post_id)
        session = db_session.create_session()
        post = session.query(Posts).get(post_id)
        categories = [category.name for category in post.categories]
        post = post.to_dict(only=('id', 'user_id', 'body'))
        user = session.query(Users).get(post['user_id'])
        post['categories'] = categories
        post['user'] = user.login
        return jsonify({'posts': post})

    def delete(self, post_id):
        posts_not_found(post_id)
        session = db_session.create_session()
        post = session.query(Posts).get(post_id)
        session.delete(post)
        session.commit()
        return jsonify({'success': f'Post {post_id} deleted'})

    def put(self, post_id):
        args = parser.parse_args()
        posts_not_found(post_id)
        session = db_session.create_session()
        post = session.query(Posts).get(post_id)
        if 'user_id' in args:
            post.user_id = args['user_id']
        if 'body' in args:
            post.body = args['body']
        if args['categories']:
            post.categories.clear()
            for cat_id in args['categories']:
                post.categories.append(session.query(Categories).get(int(cat_id)))
        session.commit()
        return jsonify({'success': 'post edited'})


class PostsListResource(Resource):
    def get(self):
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
        print(posts_)
        return jsonify(
            {'posts': posts_})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if not all(key in args for key in ['user_id', 'body']):
            return jsonify({'error': 'not enough arguments'})
        post = Posts(
            user_id=args['user_id'],
            body=args['body']
        )
        if args['categories']:
            for cat_id in args['categories']:
                if str(cat_id).isdigit():
                    post.categories.append(session.query(Categories).get(int(cat_id)))
        session.add(post)
        session.commit()
        return jsonify({'success': 'post added'})
