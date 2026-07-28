import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parents[1] / "pybo.db"


def test_release_database_is_valid():
    assert DATABASE_PATH.exists()
    with sqlite3.connect(DATABASE_PATH) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(reservation)")
        }
        missing_statuses = connection.execute(
            "SELECT COUNT(*) FROM reservation WHERE status IS NULL"
        ).fetchone()[0]
    assert "status" in columns
    assert missing_statuses == 0
