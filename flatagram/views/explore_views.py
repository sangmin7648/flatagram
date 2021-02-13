from flask import Blueprint, render_template, url_for, g
from flatagram.models import Posts, Users, db
from werkzeug.utils import redirect

bp = Blueprint('explore', __name__, url_prefix='/explore')


@bp.route('/')
def main():
    explore_post_set = Posts.query.order_by(Posts.created_date.desc())
    return render_template('explores/explore_main.html', explore_post_set=explore_post_set)
