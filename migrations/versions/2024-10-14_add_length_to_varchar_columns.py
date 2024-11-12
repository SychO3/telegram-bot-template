"""Add length to VARCHAR columns

Revision ID: c4954a09f72d
Revises:
Create Date: 2024-10-14 22:40:50.450144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'c4954a09f72d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('language_code', sa.String(length=10), nullable=True),
    sa.Column('referrer', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('is_suspicious', sa.Boolean(), nullable=False),
    sa.Column('is_block', sa.Boolean(), nullable=False),
    sa.Column('is_premium', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.drop_table('roles_admins')
    op.drop_index('name', table_name='role')
    op.drop_table('role')
    op.drop_index('email', table_name='admin')
    op.drop_index('fs_uniquifier', table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('last_name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('email', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('confirmed_at', mysql.DATETIME(), nullable=True),
    sa.Column('fs_uniquifier', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('fs_uniquifier', 'admin', ['fs_uniquifier'], unique=True)
    op.create_index('email', 'admin', ['email'], unique=True)
    op.create_table('role',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('description', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'role', ['name'], unique=True)
    op.create_table('roles_admins',
    sa.Column('admin_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('role_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], name='roles_admins_ibfk_1'),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name='roles_admins_ibfk_2'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('users')
    # ### end Alembic commands ###
