# alembic/env.py

import sys
import pathlib
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ─────────────────────────────────────────────
# Ensure root directory is in sys.path
# (so imports like "from app..." work)
# ─────────────────────────────────────────────
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

# ─────────────────────────────────────────────
# Load FastAPI settings and model metadata
# ─────────────────────────────────────────────
from app.core.config import settings
from app.models import Base

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# ─────────────────────────────────────────────
# Optional Logging setup (won't crash if missing)
# ─────────────────────────────────────────────
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except KeyError:
        # Some default alembic.ini files are missing [formatters]
        pass

# ─────────────────────────────────────────────
# Metadata for Alembic autogenerate
# ─────────────────────────────────────────────
target_metadata = Base.metadata

# ─────────────────────────────────────────────
# Run migrations offline (generates SQL script)
# ─────────────────────────────────────────────
def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# ─────────────────────────────────────────────
# Run migrations online (directly on DB)
# ─────────────────────────────────────────────
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detect column type changes
        )
        with context.begin_transaction():
            context.run_migrations()

# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
