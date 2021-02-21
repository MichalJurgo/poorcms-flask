from flask import render_template, url_for, flash, redirect, request

from poorcms import app, db
from poorcms.models import StaticPage
from poorcms.forms import StaticPageForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page/<int:page_id>')
def static_page(page_id):
    page = StaticPage.query.get_or_404(page_id)
    return render_template('static_page.html', page=page)


@app.route('/page/new', methods=['GET', 'POST'])
def new_static_page():
    form = StaticPageForm()
    if form.validate_on_submit():
        page = StaticPage(title=form.title.data, content=form.content.data,
                        in_menu=form.in_menu.data)
        db.session.add(page)
        db.session.commit()
        flash('New page created.', 'success')
        return redirect(url_for('index'))
    return render_template('new_static_page.html', form=form, legend='New page')


@app.route('/page/<int:page_id>/edit', methods=['GET', 'POST'])
def edit_static_page(page_id):
    page = StaticPage.query.get_or_404(page_id)
    form = StaticPageForm()
    if form.validate_on_submit():
        page.title = form.title.data
        page.content = form.content.data
        page.in_menu = form.in_menu.data
        page.meta_title = form.meta_title.data
        page.meta_description = form.meta_description.data
        page.meta_noindex = form.meta_noindex.data
        db.session.commit()
        flash('Page updated successfuly.', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = page.title
        form.content.data = page.content
        form.in_menu.data = page.in_menu
        form.meta_title.data = page.meta_title
        form.meta_description.data = page.meta_description
        form.meta_noindex.data = page.meta_noindex
    return render_template('new_static_page.html', form=form, edit_page=True,
                            page=page, legend='Edit page')


@app.route('/page/<int:page_id>/delete', methods=['POST'])
def delete_static_page(page_id):
    page = StaticPage.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    flash('Page deleted successfuly.', 'danger')
    return redirect(url_for('index'))


@app.context_processor
def inject_menu_pages():
    menu_pages = StaticPage.query.filter_by(in_menu=True).all()
    return dict(menu_pages=menu_pages)
