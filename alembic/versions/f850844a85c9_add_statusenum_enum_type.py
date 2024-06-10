import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f850844a85c9'
down_revision = 'd3ffb754d5e0'
branch_labels = None
depends_on = None


def upgrade():
    # Check if the enum type already exists and create if not
    op.execute("""
    DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statusenum') THEN
            CREATE TYPE statusenum AS ENUM ('alive', 'dead', 'finished');
        END IF;
    END $$;
    """)

    # Change the column to use the new enum type
    op.alter_column('users', 'status', existing_type=sa.String(),
                    type_=sa.Enum('alive', 'dead', 'finished', name='statusenum'))


def downgrade():
    # Revert the column to String type
    op.alter_column('users', 'status', existing_type=sa.Enum('alive', 'dead', 'finished', name='statusenum'),
                    type_=sa.String())

    # Drop the enum type if it exists
    op.execute("DROP TYPE IF EXISTS statusenum")
