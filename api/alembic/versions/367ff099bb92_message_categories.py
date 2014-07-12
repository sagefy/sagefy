"""Message categories

Revision ID: 367ff099bb92
Revises: 4d41b5913601
Create Date: 2014-07-12 19:55:43.829728

"""

# revision identifiers, used by Alembic.
revision = '367ff099bb92'
down_revision = '4d41b5913601'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'messages_categories',
        sa.Column('message_id', sa.String(length=64), nullable=True),
        sa.Column('category_id', sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], )
    )


def downgrade():
    op.drop_table('messages_categories')
