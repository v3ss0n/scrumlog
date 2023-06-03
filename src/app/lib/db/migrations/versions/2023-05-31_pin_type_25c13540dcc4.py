"""pin_type

Revision ID: 25c13540dcc4
Revises:
Create Date: 2023-05-31 19:23:03.422993

"""
import sqlalchemy as sa
from alembic import op
from litestar.contrib.sqlalchemy.types import GUID

__all__ = ["downgrade", "upgrade"]


sa.GUID = GUID

# revision identifiers, used by Alembic.
revision = "25c13540dcc4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "project",
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("pin", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("labels", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("documents", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("_sentinel", sa.Integer(), nullable=True),
        sa.Column("id", sa.GUID(length=16), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project")),
        sa.UniqueConstraint("slug", name=op.f("uq_project_slug")),
    )
    op.create_table(
        "team",
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.GUID(length=16), nullable=False),
        sa.Column("_sentinel", sa.Integer(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_team")),
    )
    op.create_index(op.f("ix_team_name"), "team", ["name"], unique=False)
    op.create_index(op.f("ix_team_slug"), "team", ["slug"], unique=True)
    op.create_table(
        "user_account",
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("verified_at", sa.DateTime(), nullable=True),
        sa.Column("_sentinel", sa.Integer(), nullable=True),
        sa.Column("id", sa.GUID(length=16), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_account")),
        sa.UniqueConstraint("email", name=op.f("uq_user_account_email")),
        comment="User accounts for application access",
    )
    op.create_table(
        "backlog",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("progress", sa.Enum("empty", "a_third", "two_third", "full", name="progressenum"), nullable=False),
        sa.Column("sprint_number", sa.Integer(), nullable=False),
        sa.Column("priority", sa.Enum("low", "med", "hi", name="priorityenum"), nullable=False),
        sa.Column(
            "status",
            sa.Enum("new", "started", "checked_in", "completed", "cancelled", name="statusenum"),
            nullable=False,
        ),
        sa.Column(
            "type", sa.Enum("backlog", "task", "draft", name="itemtype"), server_default="backlog", nullable=False
        ),
        sa.Column(
            "category",
            sa.Enum(
                "ideas",
                "issues",
                "maintenance",
                "finances",
                "innovation",
                "bugs",
                "features",
                "security",
                "attention",
                "backend",
                "database",
                "desktop",
                "mobile",
                "intl",
                "design",
                "analytics",
                "automation",
                name="tagenum",
            ),
            nullable=False,
        ),
        sa.Column("order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("est_days", sa.Float(), nullable=False),
        sa.Column("points", sa.Integer(), server_default="0", nullable=False),
        sa.Column("beg_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("labels", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("assignee_id", sa.GUID(length=16), nullable=True),
        sa.Column("owner_id", sa.GUID(length=16), nullable=False),
        sa.Column("project_id", sa.GUID(length=16), nullable=False),
        sa.Column("_sentinel", sa.Integer(), nullable=True),
        sa.Column("id", sa.GUID(length=16), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["assignee_id"], ["user_account.id"], name=op.f("fk_backlog_assignee_id_user_account")),
        sa.ForeignKeyConstraint(["owner_id"], ["user_account.id"], name=op.f("fk_backlog_owner_id_user_account")),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], name=op.f("fk_backlog_project_id_project")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_backlog")),
    )
    op.create_index(op.f("ix_backlog_slug"), "backlog", ["slug"], unique=True)
    op.create_index(op.f("ix_backlog_type"), "backlog", ["type"], unique=False)
    op.create_table(
        "team_invitation",
        sa.Column("team_id", sa.GUID(length=16), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("is_accepted", sa.Boolean(), nullable=False),
        sa.Column("invited_by_id", sa.GUID(length=16), nullable=True),
        sa.Column("invited_by_email", sa.String(), nullable=False),
        sa.Column("id", sa.GUID(length=16), nullable=False),
        sa.Column("_sentinel", sa.Integer(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["invited_by_id"],
            ["user_account.id"],
            name=op.f("fk_team_invitation_invited_by_id_user_account"),
            ondelete="set null",
        ),
        sa.ForeignKeyConstraint(
            ["team_id"], ["team.id"], name=op.f("fk_team_invitation_team_id_team"), ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_team_invitation")),
    )
    op.create_index(op.f("ix_team_invitation_email"), "team_invitation", ["email"], unique=False)
    op.create_table(
        "team_member",
        sa.Column("user_id", sa.GUID(length=16), nullable=False),
        sa.Column("team_id", sa.GUID(length=16), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("is_owner", sa.Boolean(), nullable=False),
        sa.Column("id", sa.GUID(length=16), nullable=False),
        sa.Column("_sentinel", sa.Integer(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["team_id"], ["team.id"], name=op.f("fk_team_member_team_id_team"), ondelete="cascade"),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user_account.id"], name=op.f("fk_team_member_user_id_user_account"), ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_team_member")),
        sa.UniqueConstraint("user_id", "team_id", name=op.f("uq_team_member_user_id")),
    )
    op.create_index(op.f("ix_team_member_role"), "team_member", ["role"], unique=False)
    op.create_table(
        "backlog_audit",
        sa.Column("backlog_id", sa.GUID(length=16), nullable=False),
        sa.Column("field_name", sa.String(), nullable=False),
        sa.Column("old_value", sa.String(), nullable=False),
        sa.Column("new_value", sa.String(), nullable=False),
        sa.Column("_sentinel", sa.Integer(), nullable=True),
        sa.Column("id", sa.GUID(length=16), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["backlog_id"], ["backlog.id"], name=op.f("fk_backlog_audit_backlog_id_backlog")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_backlog_audit")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("backlog_audit")
    op.drop_index(op.f("ix_team_member_role"), table_name="team_member")
    op.drop_table("team_member")
    op.drop_index(op.f("ix_team_invitation_email"), table_name="team_invitation")
    op.drop_table("team_invitation")
    op.drop_index(op.f("ix_backlog_type"), table_name="backlog")
    op.drop_index(op.f("ix_backlog_slug"), table_name="backlog")
    op.drop_table("backlog")
    op.drop_table("user_account")
    op.drop_index(op.f("ix_team_slug"), table_name="team")
    op.drop_index(op.f("ix_team_name"), table_name="team")
    op.drop_table("team")
    op.drop_table("project")
    # ### end Alembic commands ###