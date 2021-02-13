from flask import Blueprint, render_template, url_for, g
from flatagram.models import Posts, Users, db, Hashtags
from werkzeug.utils import redirect

bp = Blueprint('explore', __name__, url_prefix='/explore')


@bp.route('/')
def main():
    post_set = Posts.query.order_by(Posts.created_date.desc())
    return render_template('explores/explore_main.html', explore_post_set=post_set)


@bp.route('/hash/<string:hashtag>')
def render_hashtag_explore(hashtag):
    tag = Hashtags.query.filter_by(tag_text=hashtag).first()
    return render_template('explores/explore_main.html', explore_post_set=tag.post)
