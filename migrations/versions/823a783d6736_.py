"""empty message

Revision ID: 823a783d6736
Revises: 5aa87c766c58
Create Date: 2018-03-31 22:49:23.914931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '823a783d6736'
down_revision = '5aa87c766c58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_first_name_key', 'users', type_='unique')
    op.drop_constraint('users_last_name_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_last_name_key', 'users', ['last_name'])
    op.create_unique_constraint('users_first_name_key', 'users', ['first_name'])
    # ### end Alembic commands ###
