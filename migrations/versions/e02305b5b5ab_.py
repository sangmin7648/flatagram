"""empty message

Revision ID: e02305b5b5ab
Revises: 
Create Date: 2021-02-13 20:08:51.025897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e02305b5b5ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hashtags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag_text', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_hashtags'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('last_message_read_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email')),
    sa.UniqueConstraint('name', name=op.f('uq_users_name')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    op.create_table('follow',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('following_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['following_id'], ['users.id'], name=op.f('fk_follow_following_id_users'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_follow_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'following_id', name=op.f('pk_follow'))
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], name=op.f('fk_messages_recipient_id_users')),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], name=op.f('fk_messages_sender_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_messages'))
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('file_name', sa.String(length=200), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_posts_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_posts'))
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_comments_post_id_posts'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_comments_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comments'))
    )
    op.create_table('hashtag_post',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('hashtag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hashtag_id'], ['hashtags.id'], name=op.f('fk_hashtag_post_hashtag_id_hashtags'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_hashtag_post_post_id_posts'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'hashtag_id', name=op.f('pk_hashtag_post'))
    )
    op.create_table('post_like',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_post_like_post_id_posts'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_post_like_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id', name=op.f('pk_post_like'))
    )
    op.create_table('comment_like',
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], name=op.f('fk_comment_like_comment_id_comments'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_comment_like_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('comment_id', 'user_id', name=op.f('pk_comment_like'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_like')
    op.drop_table('post_like')
    op.drop_table('hashtag_post')
    op.drop_table('comments')
    op.drop_table('posts')
    op.drop_table('messages')
    op.drop_table('follow')
    op.drop_table('users')
    op.drop_table('hashtags')
    # ### end Alembic commands ###
