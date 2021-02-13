from flask import render_template

from poorcms import app
from poorcms.models import StaticPage


@app.route('/')
def index():
    return render_template('index.html')
