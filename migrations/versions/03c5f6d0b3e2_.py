"""empty message

Revision ID: 03c5f6d0b3e2
Revises: 569300a2fb67
Create Date: 2021-08-01 09:59:30.641564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03c5f6d0b3e2'
down_revision = '569300a2fb67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pack',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deck_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['deck_id'], ['deck.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.alter_column('deck', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'deck', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'deck', type_='unique')
    op.alter_column('deck', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_table('pack')
    # ### end Alembic commands ###