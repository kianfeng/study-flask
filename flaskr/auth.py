import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# create a blueprint called 'auth' and register in init.py
# blueprint is component/individual piece of application
bp = Blueprint('auth', __name__, url_prefix='/auth')


# endpoints /auth/register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # request.form: special type of dict
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # verify both value are not empty
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            # After storing the user, they are redirected to the login page
            else:
                return redirect(url_for("auth.login"))

        # If validation fails, the error is shown to the user
        flash(error)

    return render_template('auth/register.html')


# view function for login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        # fetchone() returns one row from the query. If the query returned no results, it returns None.

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session is a dict that stores data across requests.
            # When validation succeeds, the user’s id is stored in a new session
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

    flash(error)
    return render_template('auth/login.html')


# register a function run before view function
# checks if a user id is stored in session and get user info from db and store in g.user
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth/login.html'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view