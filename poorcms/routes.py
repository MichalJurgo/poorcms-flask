from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required

from poorcms import app, db
from poorcms.models import StaticPage, User, Post
from poorcms.forms import StaticPageForm, RegistrationForm, LoginForm, PostForm
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
        db.session.add(page)
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
        user = User(login=form.login.data, email=form.email.data,
                    password=form.password.data)
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
        if (user and user.verify_password(form.password.data)):
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


@app.route('/posts')
def posts():
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc())
    return render_template('posts.html', posts=posts)


@app.route('/post/<string:post_slug>')
def post(post_slug):
    post = Post.query.filter_by(slug=post_slug).first_or_404()
    return render_template('post.html', post=post)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            published=form.published.data,
            author=current_user._get_current_object()
        )
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('posts'))
    return render_template('new_post.html', form=form, legend='New post')


@app.route('/post/<string:post_slug>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_post(post_slug):
    post = Post.query.filter_by(slug=post_slug).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.published = form.published.data
        db.session.add(post)
        db.session.commit()
        flash('Post updated successfuly.', 'success')
        return redirect(url_for('post', post_slug=post.slug))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.published.data = post.published
    return render_template('new_post.html', form=form, post=post,
                            legend='Edit post', edit_post=True)


@app.route('/post/<string:post_slug>/delete', methods=['POST'])
@login_required
@admin_required
def delete_post(post_slug):
    post = Post.query.filter_by(slug=post_slug).first_or_404()
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfuly.', 'danger')
    return redirect(url_for('posts'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.context_processor
def inject_menu_pages():
    menu_pages = StaticPage.query.filter_by(in_menu=True).all()
    return dict(menu_pages=menu_pages)
