from flask import Blueprint, render_template, url_for, g, request
from flatagram.models import Posts, Users
from werkzeug.utils import redirect

from ..models import db, Posts
from .auth_views import login_required

bp = Blueprint('like', __name__, url_prefix='/like')


@bp.route('/p/<int:post_id>/')
@login_required
def post(post_id):
    _post = Posts.query.get_or_404(post_id)
    if _post in g.user.post_like_set:
        _post.like.remove(g.user)
        db.session.commit()
    else:
        _post.like.append(g.user)
        db.session.commit()
    return redirect(request.referrer)
