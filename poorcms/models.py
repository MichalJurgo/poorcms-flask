from poorcms import db


class StaticPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=True)
    in_menu = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.title
