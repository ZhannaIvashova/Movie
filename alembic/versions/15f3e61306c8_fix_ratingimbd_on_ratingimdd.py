"""fix ratingImbd on ratingIMDd

Revision ID: 15f3e61306c8
Revises: 7c03cdde8e05
Create Date: 2024-02-14 14:43:12.663865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15f3e61306c8'
down_revision: Union[str, None] = '7c03cdde8e05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ratingIMDd', sa.Float(), nullable=True))
        batch_op.drop_column('ratingImbd')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ratingImbd', sa.FLOAT(), nullable=True))
        batch_op.drop_column('ratingIMDd')

    # ### end Alembic commands ###