"""empty message

Revision ID: 621ab5af8e94
Revises: 2374bfcd64ef
Create Date: 2021-03-02 13:03:51.334351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '621ab5af8e94'
down_revision = '2374bfcd64ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=20), nullable=False),
    sa.Column('password_hash', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('role', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('login', sa.VARCHAR(length=20), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=60), nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('role', sa.VARCHAR(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###
