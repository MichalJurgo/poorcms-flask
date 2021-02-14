from flask import render_template

from poorcms import app
from poorcms.models import StaticPage


@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def inject_menu_pages():
    menu_pages = StaticPage.query.filter_by(in_menu=True).all()
    return dict(menu_pages=menu_pages)
