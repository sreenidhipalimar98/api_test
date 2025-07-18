# Alembic migration helpers
import os
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv
from shared.secrets import get_secret


load_dotenv()
def run_alembic_upgrade(db_name: str, revision: str = "head"):
    print(f"Running Alembic migrations for database: {db_name} with revision: {revision}...")
    """
    Run Alembic migrations for the given tenant database name.
    Constructs the full DB URL using environment values.
    """
    db_url = (
        f"postgresql+psycopg2://{os.getenv('dev_username')}:{os.getenv('dev_password')}"
        f"@{os.getenv('dev_host')}:{os.getenv('dev_port')}/{db_name}"
    )

    alembic_cfg = Config("shared/alembic.ini")  # path relative to your current working dir
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)

    # Optional: if you use -x options in env.py
    alembic_cfg.cmd_opts = type('obj', (object,), {'x': [f'db_url={db_url}']})

    command.upgrade(alembic_cfg, revision)

run_alembic_upgrade("naadidevdb",'000')  # Run migrations for the global DB on startup