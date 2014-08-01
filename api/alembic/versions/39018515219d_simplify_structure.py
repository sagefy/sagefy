"""Simplify structure

Revision ID: 39018515219d
Revises: 367ff099bb92
Create Date: 2014-08-01 21:10:55.293830

"""

# revision identifiers, used by Alembic.
revision = '39018515219d'
down_revision = '367ff099bb92'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('sets',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('goals',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('units',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cards',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cards_versions',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('card_id', sa.String(length=64), nullable=True),
    sa.Column('kind_tablename', sa.String(length=64), nullable=True),
    sa.Column('goal_id', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('canonical', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('units_versions',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('unit_id', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('canonical', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['unit_id'], ['units.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('goals_versions',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('goal_id', sa.String(length=64), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('canonical', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sets_versions',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('set_id', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('canonical', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['set_id'], ['sets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sets_versions_components',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('unit_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['unit_id'], ['units.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['sets_versions.id'], )
    )
    op.create_table('units_versions_prerequisites',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('prerequisite_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['prerequisite_id'], ['units.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['units_versions.id'], )
    )
    op.create_table('cards_versions_multiple_choice',
    sa.Column('version_id', sa.String(length=64), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('attempts_allowed', sa.Integer(), nullable=True),
    sa.Column('max_choices', sa.Integer(), nullable=True),
    sa.Column('multiple_correct', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['version_id'], ['cards_versions.id'], ),
    sa.PrimaryKeyConstraint('version_id')
    )
    op.create_table('cards_versions_videos',
    sa.Column('version_id', sa.String(length=64), nullable=False),
    sa.Column('duration', sa.Interval(), nullable=True),
    sa.Column('url', sa.String(length=2048), nullable=True),
    sa.ForeignKeyConstraint(['version_id'], ['cards_versions.id'], ),
    sa.PrimaryKeyConstraint('version_id')
    )
    op.create_table('cards_versions_categories',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('category_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['cards_versions.id'], )
    )
    op.create_table('cards_versions_multiple_choice_answer_text',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('correct', sa.Boolean(), nullable=True),
    sa.Column('feedback', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['version_id'], ['cards_versions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sets_versions_sets',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('child_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['sets.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['sets_versions.id'], )
    )
    op.create_table('units_goals',
    sa.Column('version_id', sa.String(length=64), nullable=True),
    sa.Column('goal_id', sa.String(length=64), nullable=True),
    sa.Column('ordinal', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['units_versions.id'], )
    )
    op.drop_table('objectives')
    op.drop_table('presentations')
    op.drop_table('components_versions')
    op.drop_table('practices_versions_categories')
    op.drop_table('practices_versions_multiple_choice')
    op.drop_table('presentations_versions_videos')
    op.drop_table('practices')
    op.drop_table('modules')
    op.drop_table('practices_versions')
    op.drop_table('presentations_versions_categories')
    op.drop_table('presentations_versions')
    op.drop_table('practices_versions_multiple_choice_answer_text')
    op.drop_table('components_versions_prerequisites')
    op.drop_table('objectives_versions')
    op.drop_table('components_objectives')
    op.drop_table('modules_versions')
    op.drop_table('modules_versions_modules')
    op.drop_table('components')
    op.drop_table('modules_versions_components')


def downgrade():
    op.create_table('modules_versions_components',
    sa.Column('version_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('component_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['component_id'], [u'components.id'], name=u'modules_versions_components_component_id_fkey'),
    sa.ForeignKeyConstraint(['version_id'], [u'modules_versions.id'], name=u'modules_versions_components_version_id_fkey')
    )
    op.create_table('components',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('language', sa.VARCHAR(length=2), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'components_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('modules_versions_modules',
    sa.Column('version_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('child_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['child_id'], [u'modules.id'], name=u'modules_versions_modules_child_id_fkey'),
    sa.ForeignKeyConstraint(['version_id'], [u'modules_versions.id'], name=u'modules_versions_modules_version_id_fkey')
    )
    op.create_table('modules_versions',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('module_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('canonical', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['module_id'], [u'modules.id'], name=u'modules_versions_module_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'modules_versions_pkey')
    )
    op.create_table('components_objectives',
    sa.Column('version_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('objective_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('ordinal', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['objective_id'], [u'objectives.id'], name=u'components_objectives_objective_id_fkey'),
    sa.ForeignKeyConstraint(['version_id'], [u'components_versions.id'], name=u'components_objectives_version_id_fkey')
    )
    op.create_table('objectives_versions',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('objective_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('canonical', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['objective_id'], [u'objectives.id'], name=u'objectives_versions_objective_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'objectives_versions_pkey')
    )
    op.create_table('components_versions_prerequisites',
    sa.Column('version_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('prerequisite_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['prerequisite_id'], [u'components.id'], name=u'components_versions_prerequisites_prerequisite_id_fkey'),
    sa.ForeignKeyConstraint(['version_id'], [u'components_versions.id'], name=u'components_versions_prerequisites_version_id_fkey')
    )
    op.create_table('practices_versions_multiple_choice_answer_text',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('version_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('correct', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('feedback', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['version_id'], [u'practices_versions.id'], name=u'practices_versions_multiple_choice_answer_text_version_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'practices_versions_multiple_choice_answer_text_pkey')
    )
    op.create_table('presentations_versions',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('presentation_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('kind_tablename', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('objective_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('canonical', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['objective_id'], [u'objectives.id'], name=u'presentations_versions_objective_id_fkey'),
    sa.ForeignKeyConstraint(['presentation_id'], [u'presentations.id'], name=u'presentations_versions_presentation_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'presentations_versions_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('presentations_versions_categories',
    sa.Column('version_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('category_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category_id'], [u'categories.id'], name=u'presentations_versions_categories_category_id_fkey'),
    sa.ForeignKeyConstraint(['version_id'], [u'presentations_versions.id'], name=u'presentations_versions_categories_version_id_fkey')
    )
    op.create_table('practices_versions',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('practice_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('kind_tablename', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('objective_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('canonical', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['objective_id'], [u'objectives.id'], name=u'practices_versions_objective_id_fkey'),
    sa.ForeignKeyConstraint(['practice_id'], [u'practices.id'], name=u'practices_versions_practice_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'practices_versions_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('modules',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('language', sa.VARCHAR(length=2), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'modules_pkey')
    )
    op.create_table('practices',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('language', sa.VARCHAR(length=2), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'practices_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('presentations_versions_videos',
    sa.Column('version_id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('duration', postgresql.INTERVAL(), autoincrement=False, nullable=True),
    sa.Column('url', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['version_id'], [u'presentations_versions.id'], name=u'presentations_versions_videos_version_id_fkey'),
    sa.PrimaryKeyConstraint('version_id', name=u'presentations_versions_videos_pkey')
    )
    op.create_table('practices_versions_multiple_choice',
    sa.Column('version_id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('attempts_allowed', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('max_choices', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('multiple_correct', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['version_id'], [u'practices_versions.id'], name=u'practices_versions_multiple_choice_version_id_fkey'),
    sa.PrimaryKeyConstraint('version_id', name=u'practices_versions_multiple_choice_pkey')
    )
    op.create_table('practices_versions_categories',
    sa.Column('version_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('category_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category_id'], [u'categories.id'], name=u'practices_versions_categories_category_id_fkey'),
    sa.ForeignKeyConstraint(['version_id'], [u'practices_versions.id'], name=u'practices_versions_categories_version_id_fkey')
    )
    op.create_table('components_versions',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('component_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('component_kind', postgresql.ENUM(u'component', u'integration', name='e1'), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('canonical', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['component_id'], [u'components.id'], name=u'components_versions_component_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'components_versions_pkey')
    )
    op.create_table('presentations',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('language', sa.VARCHAR(length=2), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'presentations_pkey')
    )
    op.create_table('objectives',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('language', sa.VARCHAR(length=2), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'objectives_pkey')
    )
    op.drop_table('units_goals')
    op.drop_table('sets_versions_sets')
    op.drop_table('cards_versions_multiple_choice_answer_text')
    op.drop_table('cards_versions_categories')
    op.drop_table('cards_versions_videos')
    op.drop_table('cards_versions_multiple_choice')
    op.drop_table('units_versions_prerequisites')
    op.drop_table('sets_versions_components')
    op.drop_table('sets_versions')
    op.drop_table('goals_versions')
    op.drop_table('units_versions')
    op.drop_table('cards_versions')
    op.drop_table('cards')
    op.drop_table('units')
    op.drop_table('goals')
    op.drop_table('sets')
