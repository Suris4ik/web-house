import os.path

from requests import get

from data.__all_models import *
from flask import Flask, render_template
from flask_login import LoginManager
from flask_restful import Api
from api.v1 import users_api, categories, posts_api
from api.v2 import users_resource, categories_resource, posts_resource
from data import db_session
from users import add_user_routes
from posts import add_post_routes
from categories import add_category_routes

app = Flask(__name__, template_folder=os.path.abspath('../templates'), static_folder=os.path.abspath('../static'))
app.config['SECRET_KEY'] = 'secret'
db_session.global_init('../db/posts.db')
session = db_session.create_session()
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
add_user_routes(app, session)
add_post_routes(app)
add_category_routes(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(Users).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    posts = get('http://localhost:8080/api/v2/posts').json()['posts']
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.register_blueprint(categories.blueprint)
    app.register_blueprint(posts_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    api.add_resource(categories_resource.CategoriesListResource, '/api/v2/categories')
    api.add_resource(categories_resource.CategoriesResource, '/api/v2/categories/<int:category_id>')
    api.add_resource(categories_resource.CategoryPosts, '/api/v2/categories/<int:category_id>/posts')
    api.add_resource(posts_resource.PostsListResource, '/api/v2/posts')
    api.add_resource(posts_resource.PostsResource, '/api/v2/posts/<int:post_id>')
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    app.run(port=8080, host='localhost')
