"""empty message

Revision ID: a99513f1be90
Revises: a4d5d7ee6789
Create Date: 2020-09-30 17:05:58.911217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a99513f1be90'
down_revision = 'a4d5d7ee6789'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('ArrayMetric_suffix_key', 'ArrayMetric', type_='unique')
    op.drop_constraint('Sfssum_suffix_key', 'Sfssum', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('Sfssum_suffix_key', 'Sfssum', ['suffix'])
    op.create_unique_constraint('ArrayMetric_suffix_key', 'ArrayMetric', ['suffix'])
    # ### end Alembic commands ###