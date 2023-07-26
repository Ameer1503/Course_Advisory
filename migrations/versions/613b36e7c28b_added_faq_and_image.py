"""added faq and image.

Revision ID: 613b36e7c28b
Revises: 1f6316aa9a03
Create Date: 2023-06-11 17:46:57.846845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '613b36e7c28b'
down_revision = '1f6316aa9a03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lecturer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_image', sa.String(length=255), nullable=True))
        batch_op.drop_column('image')

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_image', sa.String(length=255), nullable=True))
        batch_op.drop_column('image')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('profile_image')

    with op.batch_alter_table('lecturer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('profile_image')

    # ### end Alembic commands ###