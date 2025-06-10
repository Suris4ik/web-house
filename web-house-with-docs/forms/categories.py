from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.simple import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea


class EditCategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired()])
    submit = SubmitField('Done')
