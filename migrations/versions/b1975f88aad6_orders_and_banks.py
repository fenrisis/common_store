"""Orders and banks

Revision ID: b1975f88aad6
Revises: 0e2bf9f1858b
Create Date: 2024-01-27 13:00:43.334990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1975f88aad6'
down_revision: Union[str, None] = '0e2bf9f1858b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank_accounts',
                    sa.Column('account_id', sa.Integer(), nullable=False),
                    sa.Column('balance', sa.Numeric(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('account_id')
                    )
    op.create_table('orders',
                    sa.Column('order_id', sa.Integer(), nullable=False),
                    sa.Column('customer_id', sa.Integer(), nullable=False),
                    sa.Column('total_amount', sa.Numeric(), nullable=False),
                    sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('order_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('bank_accounts')
    # ### end Alembic commands ###