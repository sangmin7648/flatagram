from flask import Blueprint, render_template, url_for, request, flash, current_app, g
from werkzeug.utils import redirect, secure_filename
import os
import shutil
import re
from datetime import datetime
from flatagram.models import Posts, Comments, Hashtags,db
from flatagram.forms import UploadForm, CommentForm
from .auth_views import login_required

bp = Blueprint('post', __name__, url_prefix='/p/')


@bp.route('/<int:post_id>')
def detail(post_id, form=None):
    post = Posts.query.get_or_404(post_id)
    if form is None:
        form = CommentForm()
    return render_template('/posts/post_detail.html', post=post, form=form)


@bp.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        desc = form.desc.data
        post = Posts(user=g.user, desc=desc, created_date=datetime.now())
        db.session.add(post)
        if '#' in desc:
            hashtag_list = extract_hashtag(desc)
            for hashtag in hashtag_list:
                tag = Hashtags.query.filter_by(tag_text=hashtag).first()
                if tag is None:
                    tag = Hashtags(tag_text=hashtag)
                    db.session.add(tag)
                    db.session.commit()
                tag.post.append(post)
        db.session.commit()
        os.mkdir(os.path.join(current_app.config['UPLOAD_FOLDER'], str(post.id)))
        for file in form.img.data:
            filename = file.filename
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], str(post.id), filename))
            if post.file_name is None:
                post.file_name = filename
            else:
                post.file_name = ','.join([post.file_name, filename])
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('/posts/post_form.html', form=form)


@bp.route('/modify/<int:post_id>', methods=['GET', 'POST'])
@login_required
def modify(post_id):
    post = Posts.query.get_or_404(post_id)
    if g.user != post.user:
        flash('수정 권한이 없습니다')
        return redirect(url_for('post.detail', post_id=post_id))
    if request.method == 'POST':
        form = UploadForm()
        if form.validate_on_submit():
            form.populate_obj(post)
            post.updated_date = datetime.now()
            desc = post.desc
            if '#' in desc:
                hashtag_list = extract_hashtag(desc)
                for hashtag in hashtag_list:
                    tag = Hashtags.query.filter_by(tag_text=hashtag).first()
                    if tag is None:
                        tag = Hashtags(tag_text=hashtag)
                        db.session.add(tag)
                        db.session.commit()
                    tag.post.append(post)
            db.session.commit()
            return redirect(url_for('post.detail', post_id=post_id))

    else:
        form = UploadForm(obj=post)
    return render_template('posts/post_form.html', form=form)


@bp.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Posts.query.get_or_404(post_id)
    if g.user != post.user:
        flash('삭제 권한이 없습니다')
        return redirect(url_for('post.detail', post_id=post_id))
    else:
        shutil.rmtree(os.path.join(current_app.config['UPLOAD_FOLDER'], str(post_id)))
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('main.home'))


def extract_hashtag(desc):
    hashtag_list = re.findall('#[\w]*', desc)
    return hashtag_list
