"""empty message

Revision ID: da57795413ac
Revises: 54caf4cbb2b2
Create Date: 2022-03-16 11:48:28.828827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da57795413ac'
down_revision = '54caf4cbb2b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animal', sa.Column('image', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('animal', 'image')
    # ### end Alembic commands ###