"""add company table

Revision ID: 57fd6e8ab3c4
Revises: 001
Create Date: 2025-06-07 07:50:39.506253

"""
from alembic import op
import sqlalchemy as sa

revision = '57fd6e8ab3c4'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.create_table(
		'company',
		sa.Column('id', sa.Integer(), nullable=False),
		sa.Column('name', sa.String(length=50), nullable=False),
		sa.PrimaryKeyConstraint('id')
	)

	op.add_column(
		'parcels',
		sa.Column('company_id', sa.Integer(), nullable=True)
	)

	op.create_foreign_key(
		'fk_parcels_company_id',
		'parcels',
		'company',
		['company_id'],
		['id']
	)


def downgrade() -> None:
	op.drop_constraint('fk_parcels_company_id', 'parcels', type_='foreignkey')
	op.drop_column('parcels', 'company_id')
	op.drop_table('company')