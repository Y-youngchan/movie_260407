import os
import sqlite3
import subprocess
import sys


def test_migrations_create_reservation_status(tmp_path):
    database_path = tmp_path / "migration.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{database_path}"
    env["FLASK_APP"] = "pybo:create_app"

    result = subprocess.run(
        [sys.executable, "-m", "flask", "db", "upgrade"],
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    with sqlite3.connect(database_path) as connection:
        columns = {
            row[1]: row
            for row in connection.execute("PRAGMA table_info(reservation)")
        }
    assert "status" in columns
    status_column = columns["status"]
    assert status_column[3] == 1
    assert status_column[4] == "'RESERVED'"
