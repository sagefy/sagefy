"""improving consistency

Revision ID: 4d41b5913601
Revises: b182fbd45f9
Create Date: 2014-06-08 18:27:55.428173

"""

# revision identifiers, used by Alembic.
revision = '4d41b5913601'
down_revision = 'b182fbd45f9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('messages', sa.Column('name', sa.String(length=256), nullable=True))
    op.drop_column('messages', 'subject')
    op.add_column('notifications', sa.Column('name', sa.String(length=256), nullable=True))
    op.drop_column('notifications', 'subject')


def downgrade():
    op.add_column('notifications', sa.Column('subject', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('notifications', 'name')
    op.add_column('messages', sa.Column('subject', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('messages', 'name')
