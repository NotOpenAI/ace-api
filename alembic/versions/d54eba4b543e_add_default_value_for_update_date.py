"""make bid status and job status unique

Revision ID: d54eba4b543e
Revises: 4ed63c505ea3
Create Date: 2024-04-15 23:20:13.438784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d54eba4b543e"
down_revision: Union[str, None] = "4ed63c505ea3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "bid_status", ["value"], schema="lookup")
    op.create_unique_constraint(None, "job_status", ["value"], schema="lookup")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "job_status", schema="lookup", type_="unique")
    op.drop_constraint(None, "bid_status", schema="lookup", type_="unique")
    # ### end Alembic commands ###