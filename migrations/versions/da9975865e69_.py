"""empty message

Revision ID: da9975865e69
Revises: e75d8a17f3d0
Create Date: 2021-08-01 10:45:04.816744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da9975865e69'
down_revision = 'e75d8a17f3d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('pack_id', sa.Integer(), nullable=False))
    op.drop_constraint('card_deck_id_category_id_cue_key', 'card', type_='unique')
    op.create_unique_constraint(None, 'card', ['pack_id', 'category_id', 'cue'])
    op.drop_constraint('card_deck_id_fkey', 'card', type_='foreignkey')
    op.create_foreign_key(None, 'card', 'pack', ['pack_id'], ['id'])
    op.drop_column('card', 'deck_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('deck_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'card', type_='foreignkey')
    op.create_foreign_key('card_deck_id_fkey', 'card', 'deck', ['deck_id'], ['id'])
    op.drop_constraint(None, 'card', type_='unique')
    op.create_unique_constraint('card_deck_id_category_id_cue_key', 'card', ['deck_id', 'category_id', 'cue'])
    op.drop_column('card', 'pack_id')
    # ### end Alembic commands ###
