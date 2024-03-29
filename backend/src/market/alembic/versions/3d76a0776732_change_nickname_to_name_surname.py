"""change nickname to name + surname

Revision ID: 3d76a0776732
Revises: 76af9d60dd07
Create Date: 2023-10-14 22:52:37.114002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d76a0776732'
down_revision: Union[str, None] = '76af9d60dd07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('surname', sa.Text(), nullable=True))
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.drop_column('users', 'surname')
    op.drop_column('users', 'name')
    # ### end Alembic commands ###
