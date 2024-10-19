"""empty message

Revision ID: 1151dc55a885
Revises: 1601ac42ec94
Create Date: 2024-10-19 06:11:02.323670

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1151dc55a885'
down_revision = '1601ac42ec94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_achievements')
    op.drop_table('achievement')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('points', sa.Integer(), nullable=True))
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=150),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=150),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('location',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.drop_index('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('username', ['username'], unique=True)
        batch_op.alter_column('location',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(length=150),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=150),
               existing_nullable=False)
        batch_op.drop_column('points')

    op.create_table('achievement',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('description', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('icon', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('user_achievements',
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('achievement_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['achievement_id'], ['achievement.id'], name='user_achievements_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_achievements_ibfk_2'),
    sa.PrimaryKeyConstraint('user_id', 'achievement_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('item_request')
    # ### end Alembic commands ###
