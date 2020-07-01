"""added question and answers tables

Revision ID: 302a0d78a2cb
Revises: 
Create Date: 2020-06-28 14:55:55.821940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '302a0d78a2cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('author_id', sa.Integer),
        sa.Column('title', sa.Text),
        sa.Column('text', sa.Text),
        sa.Column('votes_up', sa.Text),
        sa.Column('votes_down', sa.Text),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'answers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('question_id', sa.Text),
        sa.Column('author_id', sa.Text),
        sa.Column('text', sa.Text),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('questions')
    op.drop_table('answers')
