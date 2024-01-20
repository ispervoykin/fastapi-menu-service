"""Change data type of column price

Revision ID: 0bcb4547e9d6
Revises: 9207ffa7f9af
Create Date: 2024-01-19 22:48:49.386608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bcb4547e9d6'
down_revision: Union[str, None] = '9207ffa7f9af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dish', 'price',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=2),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dish', 'price',
               existing_type=sa.Numeric(precision=12, scale=2),
               type_=sa.REAL(),
               existing_nullable=True)
    # ### end Alembic commands ###
