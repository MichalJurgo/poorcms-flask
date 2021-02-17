from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '7bcec7b66e868f5c5f778527803ffa81'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poorcms.db'
db = SQLAlchemy(app)


from poorcms import routes
