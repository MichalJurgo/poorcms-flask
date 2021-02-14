from flask import render_template

from poorcms import app
from poorcms.models import StaticPage


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page/<int:page_id>')
def static_page(page_id):
    page = StaticPage.query.get_or_404(page_id)
    return render_template('static_page.html', page=page)


@app.context_processor
def inject_menu_pages():
    menu_pages = StaticPage.query.filter_by(in_menu=True).all()
    return dict(menu_pages=menu_pages)
