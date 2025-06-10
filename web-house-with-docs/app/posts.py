from flask import request, redirect, render_template
from flask_login import login_required, current_user
from requests import get, put, post, delete
from werkzeug.utils import secure_filename
from forms.posts import EditPostForm


def add_post_routes(app):
    @app.route('/add/post', methods=['GET', 'POST'])
    @login_required
    def add_post():
        form = EditPostForm()
        if current_user.is_authenticated:
            if form.validate_on_submit():
                post_add = post('http://localhost:8080/api/v2/posts',
                                json={'user_id': current_user.id, 'body': form.body.data,
                                      'categories': [form.categories.data]}).json()
                if 'success' in post_add:
                    return redirect('/')
                return render_template('edit_post.html', form=form, message=post_add)
        return render_template('edit_post.html', form=form)


    @app.route('/delete/posts/<int:post_id>', methods=['GET', 'POST'])
    @login_required
    def delete_post(post_id):
        delete(f'http://localhost:8080/api/v2/posts/{post_id}')
        return redirect('/')