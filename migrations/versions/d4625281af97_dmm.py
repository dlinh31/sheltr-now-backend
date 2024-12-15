"""“dmm”

Revision ID: d4625281af97
Revises: 90318c169a58
Create Date: 2024-09-28 14:50:11.203584

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd4625281af97'
down_revision = '90318c169a58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shelter')
    op.drop_table('flood__alert')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flood__alert',
    sa.Column('id', mysql.VARCHAR(length=36), nullable=False),
    sa.Column('event', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('area_desc', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('severity', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('certainty', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('urgency', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('headline', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('description', mysql.TEXT(), nullable=False),
    sa.Column('coordinates', mysql.TEXT(), nullable=False),
    sa.Column('effective', mysql.DATETIME(), nullable=False),
    sa.Column('expires', mysql.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('shelter',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('latitude', mysql.FLOAT(), nullable=False),
    sa.Column('address', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('capacity', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('current_occupancy', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('provider_profile_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('longitude', mysql.FLOAT(), nullable=False),
    sa.ForeignKeyConstraint(['provider_profile_id'], ['provider_profile.id'], name='shelter_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###