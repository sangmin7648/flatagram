"""empty message

Revision ID: 4436ad9e26ad
Revises: 39ed3545ceac
Create Date: 2021-02-19 17:55:40.296071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4436ad9e26ad'
down_revision = '39ed3545ceac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_user_tag',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_post_user_tag_post_id_posts'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_post_user_tag_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id', name=op.f('pk_post_user_tag'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_user_tag')
    # ### end Alembic commands ###
