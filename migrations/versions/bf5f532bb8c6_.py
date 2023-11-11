"""empty message

Revision ID: bf5f532bb8c6
Revises: b8b0b96e4195
Create Date: 2021-04-23 08:40:52.821180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf5f532bb8c6'
down_revision = 'b8b0b96e4195'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Suffix', sa.Column('desc', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Suffix', 'desc')
    # ### end Alembic commands ###
