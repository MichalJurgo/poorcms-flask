from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required

from poorcms import app, db, bcrypt
from poorcms.models import StaticPage, User
from poorcms.forms import StaticPageForm, RegistrationForm, LoginForm
from poorcms.decorators import admin_required


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page/<int:page_id>')
def static_page(page_id):
    page = StaticPage.query.get_or_404(page_id)
    return render_template('static_page.html', page=page)


@app.route('/page/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_static_page():
    form = StaticPageForm()
    if form.validate_on_submit():
        page = StaticPage(title=form.title.data,
                        content=form.content.data,
                        in_menu=form.in_menu.data,
                        meta_title=form.meta_title.data,
                        meta_description=form.meta_description.data,
                        meta_noindex=form.meta_noindex.data)
        db.session.add(page)
        db.session.commit()
        flash('New page created.', 'success')
        return redirect(url_for('index'))
    return render_template('new_static_page.html', form=form, legend='New page')


@app.route('/page/<int:page_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
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
@login_required
@admin_required
def delete_static_page(page_id):
    page = StaticPage.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    flash('Page deleted successfuly.', 'danger')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(login=form.login.data, email=form.email.data,
                    password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.login.data}.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if (user and bcrypt.check_password_hash(user.password,
                form.password.data)):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Check login and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.context_processor
def inject_menu_pages():
    menu_pages = StaticPage.query.filter_by(in_menu=True).all()
    return dict(menu_pages=menu_pages)
