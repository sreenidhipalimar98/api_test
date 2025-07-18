"""Insert master datas

Revision ID: 002
Revises: 000
Create Date: 2025-07-14 23:29:31.594026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, Sequence[str], None] = '000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _execute_sql_file(conn, file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines[:-1]:  # Skip last line (e.g., summary report)
        line = line.strip()
        if line and not line.startswith('--'):
            conn.execute(sa.text(line))

def upgrade() -> None:
    conn = op.get_bind()
    file_paths = [
        'version_text_files/version01/pipe_inserts.txt',
        'version_text_files/version01/fitting_inserts.txt',
        'version_text_files/version01/gas_inserts.txt',
        'version_text_files/version01/liquid_inserts.txt',
    ]

    for path in file_paths:
        _execute_sql_file(conn, path)

def downgrade() -> None:
    pass
