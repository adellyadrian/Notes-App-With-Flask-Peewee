from flask import Flask, render_template, request, url_for, flash, redirect, abort, session
from database import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['DATABASE'] = 'database.db'


def create_tables():
    with db:
        db.create_tables([Contact, Notes])


def get_db_connection():
    db.connect()
    return db


def get_post(post_id):
    try:
        post = Notes.get_by_id(post_id)
        return post
    except Notes.DoesNotExist:
        abort(404)


@app.route('/')
def main_page():
    return render_template('home-page.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


@app.route('/AboutPage')
def about():
    return render_template('about-us.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = Contact.get(Contact.username == username)
            if user.password == password:
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('display'))
            else:
                flash('Invalid username or password.', 'error')
        except Contact.DoesNotExist:
            flash('Invalid username or password.', 'error')
    return render_template('log-in.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        new_contact = Contact.create(
            first_name=first_name,
            second_name=second_name,
            email=email,
            username=username,
            password=password
        )
        flash('Account created successfully!', 'success')
        return redirect(url_for('login_page'))
    return render_template('sign-up.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login_page'))


@app.route('/display')
def display():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Contact.get(Contact.id == user_id)
        username = session.get('username')
        return render_template('base.html', username=username)


@app.route('/all_notes')
def new1():
    notes = Notes.select()
    return render_template('block-post.html', posts=notes)


@app.route('/search', methods=['GET', 'POST'])
def search_posts():
    if request.method == 'POST':
        post_name = request.form.get('post_name', '')

        posts = Notes.select().where(Notes.headline == post_name)
        if posts.exists():
            return render_template('search_posts.html', posts=posts)
        else:
            flash('No matching posts found.', 'error')
            return redirect(url_for('search_posts'))

    return render_template('create.html')


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['headline']
        content = request.form['content_post']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            Notes.create(headline=title, content_post=content)
            return redirect(url_for('new1'))

    return render_template('create.html')


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')
        else:
            post.headline = title
            post.content_post = content
            post.save()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('new1'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete/', methods=['POST'])
def delete(id):
    post = get_post(id)
    post.delete_instance()
    flash('"{}" was successfully deleted!'.format(post.headline), 'success')
    return redirect(url_for('new1'))


if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=5006)
