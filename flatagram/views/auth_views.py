from flask import Blueprint, url_for, request, render_template, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import functools

from flatagram.models import db, Users
from flatagram.forms import UserCreateForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if not user:
            user = Users(username=form.username.data,
                         name=form.name.data,
                         password=generate_password_hash(form.password1.data),
                         email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            flash('이미 사용중인 아이디입니다.')
    return render_template('/auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        error = None
        user = Users.query.filter(
            (Users.username == form.username_or_email.data) |
            (Users.email == form.username_or_email.data)).first()
        if not user:
            error = "존재하지 않는 계정입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 잘못되었습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.home'))
        flash(error)
    return render_template('/auth/login.html', form=form)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.home'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.get(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
