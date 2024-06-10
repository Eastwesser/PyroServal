from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'revision_id'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE TYPE statusenum AS ENUM ('alive', 'dead', 'unknown')")
    # Modify existing table to use the new enum type if needed
    op.alter_column('users', 'status', existing_type=sa.String(), type_=sa.Enum('alive', 'dead', 'unknown', name='statusenum'))

def downgrade():
    op.alter_column('users', 'status', existing_type=sa.Enum('alive', 'dead', 'unknown', name='statusenum'), type_=sa.String())
    op.execute("DROP TYPE statusenum")
