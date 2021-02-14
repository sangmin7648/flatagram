from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))


post_like_table = db.Table(
    'post_like',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True))

comment_like_table = db.Table(
    'comment_like',
    db.Column('comment_id', db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True))

follow_table = db.Table(
    'follow',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('following_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True))

hashtag_post_table = db.Table(
    'hashtag_post',
    db.Column('post_id', db.Integer,  db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtags.id', ondelete='CASCADE'), primary_key=True))

saved_post_table = db.Table(
    'saved_post',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True))


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('Users', backref=db.backref('post_set'))
    file_name = db.Column(db.String(200))
    desc = db.Column(db.Text(), nullable=True)
    created_date = db.Column(db.DateTime(), nullable=False)
    updated_date = db.Column(db.DateTime(), nullable=True)
    like = db.relationship('Users', secondary=post_like_table, backref=db.backref('post_like_set'))


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('Users', backref=db.backref('comment_set'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'))
    post = db.relationship('Posts', backref=db.backref('comment_set'))
    comment = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False)
    updated_date = db.Column(db.DateTime(), nullable=True)
    like = db.relationship('Users', secondary=comment_like_table, backref=db.backref('comment_like_set'))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    last_message_read_time = db.Column(db.DateTime())
    messages_sent = db.relationship('Messages', foreign_keys='Messages.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Messages', foreign_keys='Messages.recipient_id',
                                        backref='recipient', lazy='dynamic')
    saved_post = db.relationship('Posts', secondary=saved_post_table)
    following = db.relationship('Users', secondary=follow_table,
                                primaryjoin=(id == follow_table.c.user_id),
                                secondaryjoin=(id == follow_table.c.following_id),
                                backref=db.backref('followers'))

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Messages.query.filter_by(recipient=self).filter(
            Messages.timestamp > last_read_time).count()


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime())


class Hashtags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_text = db.Column(db.String(50), nullable=False)
    post = db.relationship('Posts', secondary=hashtag_post_table, backref=db.backref('post_hashtag_set'))
