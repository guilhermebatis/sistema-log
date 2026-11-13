"""update database schema

Revision ID: e99918d7561a
Revises: e240484b932e
Create Date: 2026-11-04 21:25:12.539921

"""
from alembic import op
import sqlalchemy as sa

revision = 'e99918d7561a'
down_revision = 'e240484b932e'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.create_unique_constraint(
            'uq_client_phone',
            ['phone']
        )

    with op.batch_alter_table('delivery_item', schema=None) as batch_op:
        batch_op.drop_constraint(
            'delivery_item_ibfk_1',
            type_='foreignkey'
        )
        batch_op.create_foreign_key(
            'fk_delivery_item_delivery_id',
            'delivery',
            ['delivery_id'],
            ['id'],
            ondelete='CASCADE'
        )


def downgrade():
    with op.batch_alter_table('delivery_item', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_delivery_item_delivery_id',
            type_='foreignkey'
        )
        batch_op.create_foreign_key(
            'delivery_item_ibfk_1',
            'delivery',
            ['delivery_id'],
            ['id']
        )

    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.drop_constraint(
            'uq_client_phone',
            type_='unique'
        )