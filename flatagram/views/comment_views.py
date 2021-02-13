from datetime import datetime

from flask import Blueprint, url_for, request, g, flash, render_template
from werkzeug.utils import redirect

from flatagram.models import db, Posts, Comments
from flatagram.forms import CommentForm
from .auth_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/<int:post_id>', methods=['POST'])
@login_required
def create(post_id):
    post = Posts.query.get(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comments(user=g.user, comment=form.comment.data, created_date=datetime.now())
        post.comment_set.append(comment)
        db.session.commit()
    return redirect(url_for('post.detail', post_id=post_id))


@bp.route('/modify/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def modify(comment_id):
    comment = Comments.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정 권한이 없습니다')
        return redirect(url_for('post.detail', post_id=comment.post_id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.updated_date = datetime.now()
            db.session.commit()
            return redirect(url_for('post.detail', post_id=comment.post_id))
    else:
        form = CommentForm(obj=comment)
        return render_template('comments/comment_form.html', form=form)


@bp.route('/delete/<int:comment_id>')
@login_required
def delete(comment_id):
    comment = Comments.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('삭제 권한이 없습니다')
        return redirect(url_for('post.detail', post_id=comment.post_id))
    else:
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('post.detail', post_id=comment.post_id))
