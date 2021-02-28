from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, BooleanField, SubmitField,
                        PasswordField)
from wtforms.validators import (DataRequired, Length, EqualTo, Email,
                                ValidationError)

from poorcms.models import User


class StaticPageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    in_menu = BooleanField('In menu')
    submit = SubmitField('Submit')
    meta_title = StringField('Meta title')
    meta_description = StringField('Meta description')
    meta_noindex = BooleanField('Noindex')


class RegistrationForm(FlaskForm):
    login = StringField('Login',
                        validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
                                    validators=[DataRequired(),
                                                EqualTo('password')])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('This login is invalid.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is invalid.')


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
