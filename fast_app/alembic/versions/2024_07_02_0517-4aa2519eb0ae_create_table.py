"""Create table

Revision ID: 4aa2519eb0ae
Revises: 
Create Date: 2024-07-02 05:17:58.056184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4aa2519eb0ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('message_user', sa.String(), nullable=False),
    sa.Column('message_ai', sa.String(), nullable=False),
    sa.Column('datetime', sa.TIMESTAMP(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chats')
    # ### end Alembic commands ###
