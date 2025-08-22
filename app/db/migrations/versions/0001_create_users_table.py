from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("user", "admin", name="role_enum"), nullable=False, server_default="user"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    # If you want a non-unique index on email (in addition to the unique constraint), uncomment:
    # op.create_index("ix_users_email", "users", ["email"], unique=False)

def downgrade():
    # Drop table first (this also drops the unique index on email)
    op.drop_table("users")
    # Only Postgres creates a named ENUM type; guard the DROP TYPE for non-sqlite dialects
    bind = op.get_bind()
    if bind.dialect.name not in ("sqlite",):
        op.execute("DROP TYPE IF EXISTS role_enum")
