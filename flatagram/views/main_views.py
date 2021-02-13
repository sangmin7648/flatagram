from flask import Blueprint, render_template, url_for, g, request
from flatagram.models import Posts, Users, db, Hashtags
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='')


@bp.route('/wip')
def work_in_progress():
    return render_template('work_in_progress.html')


@bp.route('/')
def home():
    if g.user:
        follow_id_list = [user.id for user in g.user.following]
        follow_id_list.append(g.user.id)
        post_list = db.session.query(Posts).\
            filter(Posts.user_id.in_(follow_id_list)).\
            order_by(Posts.created_date.desc()).all()
        return render_template('home.html', post_list=post_list)
    else:
        return redirect(url_for('auth.login'))


@bp.route('/search')
def search():
    keyword = request.values.get('keyword')
    user_list = [user for user in Users.query.filter(Users.name.like('%'+keyword+'%'))]
    hashtag_list = [hashtag for hashtag in Hashtags.query.filter(Hashtags.tag_text.like('%'+keyword+'%'))]
    return render_template('search.html', user_list=user_list, hashtag_list=hashtag_list)

