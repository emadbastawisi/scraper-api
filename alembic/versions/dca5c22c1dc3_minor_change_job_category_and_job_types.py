"""minor change job category and job types

Revision ID: dca5c22c1dc3
Revises: bb086fbed31c
Create Date: 2023-09-14 18:18:43.746421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dca5c22c1dc3'
down_revision: Union[str, None] = 'bb086fbed31c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_career_interests', sa.Column('years_of_experience', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_career_interests', 'years_of_experience')
    # ### end Alembic commands ###
