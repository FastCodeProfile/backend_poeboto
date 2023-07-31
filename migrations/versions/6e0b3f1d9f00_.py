"""empty message

Revision ID: 6e0b3f1d9f00
Revises: 
Create Date: 2023-07-29 00:53:34.077416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e0b3f1d9f00'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ban', sa.Boolean(), nullable=False),
    sa.Column('api_id', sa.Integer(), nullable=False),
    sa.Column('api_hash', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('lang_code', sa.String(), nullable=False),
    sa.Column('app_version', sa.String(), nullable=False),
    sa.Column('device_model', sa.String(), nullable=False),
    sa.Column('session_string', sa.String(), nullable=False),
    sa.Column('last_call', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('proxies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scheme', sa.String(), nullable=False),
    sa.Column('rotation_url', sa.String(), nullable=False),
    sa.Column('ip', sa.String(), nullable=False),
    sa.Column('busy', sa.Boolean(), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_super', sa.Boolean(), nullable=False),
    sa.Column('balance', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('subscribers_tasks',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('url_avatar', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('pause', sa.Boolean(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('in_progress', sa.Boolean(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('count_done', sa.Integer(), nullable=False),
    sa.Column('skip_bots', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('views_tasks',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('limit', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('url_avatar', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('pause', sa.Boolean(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('in_progress', sa.Boolean(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('count_done', sa.Integer(), nullable=False),
    sa.Column('skip_bots', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('views_tasks')
    op.drop_table('subscribers_tasks')
    op.drop_table('users')
    op.drop_table('proxies')
    op.drop_table('bots')
    # ### end Alembic commands ###
