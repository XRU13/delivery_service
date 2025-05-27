"""initial

Revision ID: 001
Revises: 
Create Date: 2024-03-19 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'parcel_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'parcels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('weight', sa.Float(), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=False),
        sa.Column('content_value_usd', sa.Float(), nullable=False),
        sa.Column('delivery_price', sa.Float(), nullable=True),
        sa.Column('session_id', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_processed', sa.Boolean(), server_default='0'),
        sa.ForeignKeyConstraint(['type_id'], ['parcel_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_parcels_session_id', 'parcels', ['session_id'])

    op.bulk_insert(
        sa.table('parcel_types',
            sa.column('name', sa.String)
        ),
        [
            {'name': 'одежда'},
            {'name': 'электроника'},
            {'name': 'разное'}
        ]
    )

def downgrade():
    op.drop_table('parcels')
    op.drop_table('parcel_types') 