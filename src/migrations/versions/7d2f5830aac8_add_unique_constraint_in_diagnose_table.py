"""add unique constraint in diagnose table

Revision ID: 7d2f5830aac8
Revises: 6999a74674f3
Create Date: 2024-05-16 15:39:39.584227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d2f5830aac8'
down_revision = '6999a74674f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('diagnose', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['task_id', 'case_id', 'user_email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('diagnose', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
