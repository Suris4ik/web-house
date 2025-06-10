from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea
from requests import get

class EditPostForm(FlaskForm):
    body = StringField('Post', widget=TextArea(), validators=[DataRequired()])

    categories = SelectMultipleField('Categories')
    submit = SubmitField('Done')

    def __init__(self):
        super(EditPostForm, self).__init__()
        categs = get('http://localhost:8080/api/v2/categories').json()['categories']
        self.categories.choices = [(int(cat['id']), str(cat['name'])) for cat in categs]