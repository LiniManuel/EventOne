"""add comments and reservations

Revision ID: dcba2dd2719f
Revises: ff15f6f2221f
Create Date: 2025-03-11 18:49:58.808872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dcba2dd2719f'
down_revision: Union[str, None] = 'ff15f6f2221f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('num_guests', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('events', sa.Column('date', sa.DateTime(timezone=True), nullable=False))
    op.add_column('events', sa.Column('capacity', sa.Integer(), nullable=False))
    op.add_column('events', sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=False))
    op.add_column('events', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.drop_constraint('events_user_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key(None, 'events', 'users', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.add_column('users', sa.Column('username', sa.Text(), nullable=False))
    op.add_column('users', sa.Column('email', sa.Text(), nullable=False))
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    op.create_unique_constraint(None, 'users', ['email'])
    op.drop_column('users', 'isAdmin')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('isAdmin', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'email')
    op.drop_column('users', 'username')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.create_foreign_key('events_user_id_fkey', 'events', 'users', ['user_id'], ['id'])
    op.drop_column('events', 'created_at')
    op.drop_column('events', 'content')
    op.drop_column('events', 'capacity')
    op.drop_column('events', 'date')
    op.drop_table('reservations')
    op.drop_table('comments')
    # ### end Alembic commands ###
