from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class StaticPageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    in_menu = BooleanField('In menu')
    submit = SubmitField('Submit')
    meta_title = StringField('Meta title')
    meta_description = StringField('Meta description')
    meta_noindex = BooleanField('Noindex')
