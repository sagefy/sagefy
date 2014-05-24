"""Starting contribution tables

Revision ID: 370653b46677
Revises: 18b60b17e4c9
Create Date: 2014-05-24 22:32:26.014136

"""

# revision identifiers, used by Alembic.
revision = '370653b46677'
down_revision = '18b60b17e4c9'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table('objectives',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('modules',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discussions_threads',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('kind_id', sa.String(length=64), nullable=True),
    sa.Column('kind_tablename', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('components',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('practices',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('presentations',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('proposals',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('kind_id', sa.String(length=64), nullable=True),
    sa.Column('kind_tablename', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('presentations_versions',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('presentation_id', sa.String(length=64), nullable=True),
    sa.Column('kind_tablename', sa.String(length=64), nullable=True),
    sa.Column('objective_id', sa.String(length=64), nullable=True),
    sa.Column('canonical', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['objective_id'], ['objectives.id'], ),
    sa.ForeignKeyConstraint(['presentation_id'], ['presentations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('modules_versions',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('module_id', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('canonical', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discussions_messages',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('thread_id', sa.String(length=64), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('replies_to_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['replies_to_id'], ['discussions_messages.id'], ),
    sa.ForeignKeyConstraint(['thread_id'], ['discussions_threads.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_notifications_settings',
    sa.Column('user_id', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('users_roles',
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Enum('admin', name='e5'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('components_versions',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('component_id', sa.String(length=64), nullable=True),
    sa.Column('component_kind', sa.Enum('component', 'integration', name='e1'), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('canonical', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['component_id'], ['components.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('objectives_versions',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('objective_id', sa.String(length=64), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('canonical', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['objective_id'], ['objectives.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('practices_versions',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('practice_id', sa.String(length=64), nullable=True),
    sa.Column('kind_tablename', sa.String(length=64), nullable=True),
    sa.Column('objective_id', sa.String(length=64), nullable=True),
    sa.Column('canonical', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['objective_id'], ['objectives.id'], ),
    sa.ForeignKeyConstraint(['practice_id'], ['practices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('presentations_versions_videos',
    sa.Column('version_id', sa.String(length=64), nullable=False),
    sa.Column('duration', sa.Interval(), nullable=True),
    sa.Column('url', sa.String(length=2048), nullable=True),
    sa.ForeignKeyConstraint(['version_id'], ['presentations_versions.id'], ),
    sa.PrimaryKeyConstraint('version_id')
    )
    op.create_table('notifications_categories',
    sa.Column('notification_id', sa.String(length=64), nullable=True),
    sa.Column('category_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['notification_id'], ['notifications.id'], )
    )
    op.create_table('modules_versions_modules',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('child_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['modules.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['modules_versions.id'], )
    )
    op.create_table('practices_versions_multiple_choice',
    sa.Column('version_id', sa.String(length=64), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('attempts_allowed', sa.Integer(), nullable=True),
    sa.Column('max_choices', sa.Integer(), nullable=True),
    sa.Column('multiple_correct', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['version_id'], ['practices_versions.id'], ),
    sa.PrimaryKeyConstraint('version_id')
    )
    op.create_table('components_versions_prerequisites',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('prerequisite_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['prerequisite_id'], ['components.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['components_versions.id'], )
    )
    op.create_table('proposals_versions',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('proposal_id', sa.String(length=64), nullable=True),
    sa.Column('kind_version_id', sa.String(length=64), nullable=True),
    sa.Column('action', sa.Enum('create', 'update', 'delete', 'split', 'merge', name='e2'), nullable=True),
    sa.Column('decision', sa.Enum('pending', 'blocked', 'accepted', 'declined', name='e3'), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['proposal_id'], ['proposals.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('components_objectives',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('objective_id', sa.String(length=64), nullable=True),
    sa.Column('ordinal', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['objective_id'], ['objectives.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['components_versions.id'], )
    )
    op.create_table('practices_versions_multiple_choice_answer_text',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('correct', sa.Boolean(), nullable=True),
    sa.Column('feedback', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['version_id'], ['practices_versions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('presentations_versions_categories',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('category_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['presentations_versions.id'], )
    )
    op.create_table('modules_versions_components',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('component_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['component_id'], ['components.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['modules_versions.id'], )
    )
    op.create_table('practices_versions_categories',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('category_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['practices_versions.id'], )
    )
    op.create_table('votes',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('proposal_version_id', sa.String(length=64), nullable=True),
    sa.Column('action', sa.Enum('agree', 'consent', 'discuss', 'dissent', name='e4'), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['proposal_version_id'], ['proposals_versions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'messages', sa.Column('from_user_id', sa.String(length=64), nullable=True))
    op.drop_column(u'messages', 'kind')
    op.drop_column(u'messages', 'modified')
    op.drop_column(u'notifications', 'kind')
    op.drop_column(u'notifications', 'modified')


def downgrade():
    op.add_column(u'notifications', sa.Column('modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column(u'notifications', sa.Column('kind', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column(u'messages', sa.Column('modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column(u'messages', sa.Column('kind', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_column(u'messages', 'from_user_id')
    op.drop_table('votes')
    op.drop_table('practices_versions_categories')
    op.drop_table('modules_versions_components')
    op.drop_table('presentations_versions_categories')
    op.drop_table('practices_versions_multiple_choice_answer_text')
    op.drop_table('components_objectives')
    op.drop_table('proposals_versions')
    op.drop_table('components_versions_prerequisites')
    op.drop_table('practices_versions_multiple_choice')
    op.drop_table('modules_versions_modules')
    op.drop_table('notifications_categories')
    op.drop_table('presentations_versions_videos')
    op.drop_table('practices_versions')
    op.drop_table('objectives_versions')
    op.drop_table('components_versions')
    op.drop_table('users_roles')
    op.drop_table('users_notifications_settings')
    op.drop_table('discussions_messages')
    op.drop_table('modules_versions')
    op.drop_table('presentations_versions')
    op.drop_table('proposals')
    op.drop_table('categories')
    op.drop_table('presentations')
    op.drop_table('practices')
    op.drop_table('components')
    op.drop_table('discussions_threads')
    op.drop_table('modules')
    op.drop_table('objectives')
