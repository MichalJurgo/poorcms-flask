from poorcms import db


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
