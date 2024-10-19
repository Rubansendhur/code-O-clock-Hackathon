"""Recreate missing migration

Revision ID: 3667e3b5ed0e
Revises: ec7cb6cad49d
Create Date: 2024-10-19 06:01:44.201692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3667e3b5ed0e'
down_revision = 'ec7cb6cad49d'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
