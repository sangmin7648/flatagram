from flask import Blueprint, render_template, url_for, g, flash, request, current_app
from ..models import Messages, Users, db
from ..forms import MessageForm
from .auth_views import login_required
from werkzeug.utils import redirect
from datetime import datetime

bp = Blueprint('dm', __name__, url_prefix='/direct')


@bp.route('/send/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = Users.query.filter_by(name=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Messages(author=g.user, recipient=user, text=form.message.data, timestamp=datetime.now())
        db.session.add(msg)
        db.session.commit()
        flash('메시지가 전송되었습니다')
        return redirect(url_for('user.profile', name=recipient))
    return render_template('DM/send_message.html', form=form, recipient=recipient)


@bp.route('/inbox')
@login_required
def inbox():
    g.user.last_message_read_time = datetime.now()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = g.user.messages_received.order_by(Messages.timestamp.desc())
    return render_template('DM/inbox_message.html', messages=messages)
