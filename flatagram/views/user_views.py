from flask import Blueprint, render_template, url_for, g, request, flash
from flatagram.models import Posts, Users, db
from werkzeug.utils import redirect
from .auth_views import login_required

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/<string:name>/')
def profile(name):
    user = Users.query.filter_by(name=name).first()
    return render_template('profile.html', user=user, post_list=user.post_set)


@bp.route('/<string:name>/saved')
def profile_saved(name):
    user = Users.query.filter_by(name=name).first()
    return render_template('profile.html', user=user, post_list=user.saved_post)


@bp.route('/<string:name>/tagged')
def profile_tagged(name):
    user = Users.query.filter_by(name=name).first()
    return render_template('profile.html', user=user, post_list=user.post_tag_set)


@bp.route('/follow/<follow_name>')
@login_required
def follow(follow_name):
    user_to_follow = Users.query.filter_by(name=follow_name).first()
    if g.user != user_to_follow:
        g.user.following.append(user_to_follow)
        db.session.commit()
    else:
        flash("스스로를 팔로우할 수 없습니다")
    return redirect(request.referrer)


@bp.route('/unfollow/<unfollow_name>')
@login_required
def unfollow(unfollow_name):
    user_to_unfollow = Users.query.filter_by(name=unfollow_name).first()
    if user_to_unfollow in g.user.following:
        g.user.following.remove(user_to_unfollow)
        db.session.commit()
    else:
        flash("팔로우하고 있지 않습니다")
    return redirect(request.referrer)


@bp.route('/<string:name>/follower')
def show_follower(name):
    user = Users.query.filter_by(name=name).first()
    follower_list = user.followers
    return render_template('/follow/follower.html', follower_list=follower_list)


@bp.route('/<string:name>/following')
def show_following(name):
    user = Users.query.filter_by(name=name).first()
    following_list = user.following
    return render_template('/follow/following.html', following_list=following_list)
