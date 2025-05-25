"""Event embeddings

Revision ID: dcefbdf2f6e1
Revises: 3ee5d6537bb1
Create Date: 2025-05-23 09:21:27.407470
"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = 'dcefbdf2f6e1'
down_revision = '3ee5d6537bb1'
branch_labels = None
depends_on = None


def upgrade():
    # 1) Ensure the pgvector extension exists
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 2) Add the embedding column
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('embedding', Vector(1536), nullable=True)
        )

    # 3) Create an IVFFlat index for fast vector search
    op.create_index(
        'ix_event_embedding',
        'event',
        ['embedding'],
        postgresql_using='ivfflat',
        postgresql_ops={'embedding': 'vector_cosine_ops'},
        postgresql_with={'lists': '100'}
    )


def downgrade():
    # 1) Drop the index
    op.drop_index('ix_event_embedding', table_name='event')

    # 2) Remove the embedding column
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('embedding')
