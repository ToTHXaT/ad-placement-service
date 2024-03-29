"""deleted hidden column from Advert table

Revision ID: 82cd8a3085d9
Revises: e5e70a132a75
Create Date: 2024-03-07 13:19:18.749523

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "82cd8a3085d9"
down_revision: Union[str, None] = "e5e70a132a75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("Advert", "is_hidden")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "Advert",
        sa.Column("is_hidden", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )
    # ### end Alembic commands ###
