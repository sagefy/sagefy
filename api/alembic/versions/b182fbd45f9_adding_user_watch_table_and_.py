"""Adding user watch table and presentation add name column

Revision ID: b182fbd45f9
Revises: 370653b46677
Create Date: 2014-05-31 04:18:46.597922

"""

# revision identifiers, used by Alembic.
revision = 'b182fbd45f9'
down_revision = '370653b46677'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users_watches',
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('kind_tablename', sa.String(length=64), nullable=True),
    sa.Column('kind_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.add_column(u'presentations_versions', sa.Column('name', sa.String(length=256), nullable=True))


def downgrade():
    op.drop_column(u'presentations_versions', 'name')
    op.drop_table('users_watches')
