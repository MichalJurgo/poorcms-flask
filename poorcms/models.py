from flask_login import UserMixin

from poorcms import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class StaticPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=True)
    in_menu = db.Column(db.Boolean, default=False)
    # Meta values
    meta_title = db.Column(db.String(128), nullable=True)
    meta_description = db.Column(db.String(256), nullable=True)
    meta_noindex = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.title


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    role = db.Column(db.String(32), default='user')

    def __repr__(self):
        return self.login
