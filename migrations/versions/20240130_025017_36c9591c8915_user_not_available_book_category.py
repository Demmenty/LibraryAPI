"""refresh_token

Revision ID: 36c9591c8915
Revises: 1dee96f8288a
Create Date: 2024-01-30 02:50:17.604159

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '36c9591c8915'
down_revision: Union[str, None] = '1dee96f8288a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refresh_token',
    sa.Column('uuid', postgresql.UUID(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('refresh_token_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', name=op.f('refresh_token_pkey'))
    )
    op.create_index(op.f('refresh_token_uuid_idx'), 'refresh_token', ['uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('refresh_token_uuid_idx'), table_name='refresh_token')
    op.drop_table('refresh_token')
    # ### end Alembic commands ###
