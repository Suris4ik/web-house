from flask import request, redirect, render_template
from flask_login import login_required, current_user
from requests import get, put, post, delete
from werkzeug.utils import secure_filename
from forms.categories import EditCategoryForm


def add_category_routes(app):
    @app.route('/add/category', methods=['GET', 'POST'])
    @login_required
    def add_category():
        form = EditCategoryForm()
        if current_user.is_authenticated:
            if form.validate_on_submit():
                category_add = post('http://localhost:8080/api/v2/categories',
                                    json={'name': form.name.data}).json()
                if 'success' in category_add:
                    return redirect('/')
        return render_template('edit_category.html', form=form)

    @app.route('/categories')
    def categories_all():
        categories = get('http://localhost:8080/api/v2/categories').json()['categories']
        return render_template('categories.html', categories=categories)

    @app.route('/categories/d/<int:category_id>', methods=['GET'])
    def category_description(category_id):
        category = get(f'http://localhost:8080/api/v2/categories/{category_id}').json()['categories']
        posts = get(f'http://localhost:8080/api/v2/categories/{category_id}/posts').json()['posts']
        return render_template('category_description.html', category=category, posts=posts)

    @app.route('/categories/<int:category_id>', methods=['GET', 'POST'])
    def edit_category(category_id):
        category = get(f'http://localhost:8080/api/v2/categories/{category_id}').json()['categories']
        form = EditCategoryForm()
        if current_user.is_admin:
            if request.method == 'GET':
                form.name.data = category['name']
            if form.validate_on_submit():
                category_update = put(f'http://localhost:8080/api/v2/categories/{category_id}',
                                      json={'name': form.name.data}).json()
                if 'success' in category_update:
                    return redirect(f'/categories')
        return render_template('edit_category.html', form=form)