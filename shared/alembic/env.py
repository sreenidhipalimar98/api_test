from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
import sys
import os
from dotenv import load_dotenv


# Ensure project base path is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import models
from models import Base

# Load environment variables from .env
load_dotenv()

# Get Alembic Config
config = context.config

# Configure logging
fileConfig(config.config_file_name)

# Set metadata
target_metadata = Base.metadata

# Build DB URL from env
def get_database_url():
    db_url = context.get_x_argument(as_dictionary=True).get("db_url")
    if db_url:
        print(f"Using db_url from CLI args: {db_url}")
        return db_url

    from dotenv import load_dotenv
    load_dotenv()

    user = os.getenv('dev_username')
    password = os.getenv('dev_password')
    host = os.getenv('dev_host')
    port = os.getenv('dev_port')
    db = os.getenv('dev_dbname')

    if not all([user, password, host, port, db]):
        raise Exception("Missing one or more DB env vars (check .env or environment)")

    print(f"Connecting to DB: {user}@{host}:{port}/{db}")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def run_migrations_offline():
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    url = get_database_url()
    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
