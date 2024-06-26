"""Create diagnose_config table

Revision ID: d479d2b24182
Revises: 7d2f5830aac8
Create Date: 2024-06-21 15:53:27.917049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd479d2b24182'
down_revision = '7d2f5830aac8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('diagnose_config',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('config', sa.JSON(), nullable=False),
    sa.Column('created_timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('diagnose_config')
    # ### end Alembic commands ###
