"""minor update

Revision ID: a1d5cbbbcd4d
Revises: dbfc9b1a6888
Create Date: 2023-09-07 20:52:13.111639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1d5cbbbcd4d'
down_revision: Union[str, None] = 'dbfc9b1a6888'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_education', sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))
    op.add_column('users_work_experience', sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))
    op.drop_constraint('users_work_experience_user_id_key', 'users_work_experience', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_work_experience_user_id_key', 'users_work_experience', ['user_id'])
    op.drop_column('users_work_experience', 'updated_at')
    op.drop_column('users_education', 'updated_at')
    # ### end Alembic commands ###
