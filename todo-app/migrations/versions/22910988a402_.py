"""empty message

Revision ID: 22910988a402
Revises: f847bfbe51bd
Create Date: 2021-06-09 19:15:32.662133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22910988a402'
down_revision = 'f847bfbe51bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todolists', sa.Column('completed', sa.Boolean(), nullable=True))

    op.execute('UPDATE todolists SET completed = False WHERE completed is NULL;')
    op.alter_column('todolists', 'completed', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todolists', 'completed')
    # ### end Alembic commands ###