"""initialize tables

Revision ID: c0e48290a8c3
Revises: 
Create Date: 2024-04-07 01:27:18.489228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c0e48290a8c3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("create schema lookup")
    op.create_table(
        "customer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("owner", sa.String(length=100), nullable=True),
        sa.Column("market", sa.String(length=50), nullable=True),
        sa.Column("reputation", sa.Integer(), nullable=True),
        sa.Column("fin_health", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customer_name"), "customer", ["name"], unique=True)
    op.create_table(
        "bid_attribute_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="lookup",
    )
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="lookup",
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table(
        "bid",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("lead", sa.String(length=100), nullable=True),
        sa.Column("foreman", sa.String(length=100), nullable=True),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.Column("finish_date", sa.DateTime(), nullable=True),
        sa.Column(
            "original_contract", sa.Numeric(precision=15, scale=2), nullable=True
        ),
        sa.Column("original_cost", sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customer.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "customer_contact",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customer.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bid_attribute_option",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("attribute_type_id", sa.Integer(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("value", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["attribute_type_id"],
            ["lookup.bid_attribute_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="lookup",
    )
    op.create_table(
        "user_role",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["lookup.role.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
    )
    op.create_table(
        "bid_attribute",
        sa.Column("bid_id", sa.Integer(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("num_val", sa.Integer(), nullable=True),
        sa.Column("option_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "(num_val IS NULL AND option_id IS NOT NULL) OR (num_val IS NOT NULL AND option_id IS NULL)",
            name="only_one_required",
        ),
        sa.ForeignKeyConstraint(
            ["bid_id"],
            ["bid.id"],
        ),
        sa.ForeignKeyConstraint(
            ["option_id"],
            ["lookup.bid_attribute_option.id"],
        ),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["lookup.bid_attribute_type.id"],
        ),
        sa.PrimaryKeyConstraint("bid_id", "type_id"),
    )
    op.create_table(
        "bid_manager",
        sa.Column("manager_id", sa.Integer(), nullable=False),
        sa.Column("bid_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["bid_id"],
            ["bid.id"],
        ),
        sa.ForeignKeyConstraint(
            ["manager_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("manager_id", "bid_id"),
    )
    op.create_table(
        "project_manager",
        sa.Column("manager_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["manager_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["bid.id"],
        ),
        sa.PrimaryKeyConstraint("manager_id", "project_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("project_manager")
    op.drop_table("bid_manager")
    op.drop_table("bid_attribute")
    op.drop_table("user_role")
    op.drop_table("bid_attribute_option", schema="lookup")
    op.drop_table("customer_contact")
    op.drop_table("bid")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_table("user")
    op.drop_table("role", schema="lookup")
    op.drop_table("bid_attribute_type", schema="lookup")
    op.drop_index(op.f("ix_customer_name"), table_name="customer")
    op.drop_table("customer")
    op.execute("drop schema lookup")
    # ### end Alembic commands ###
