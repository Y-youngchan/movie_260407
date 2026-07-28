import importlib
from pathlib import Path

import pytest


@pytest.mark.filterwarnings("error::sqlalchemy.exc.LegacyAPIWarning")
def test_authenticated_user_can_open_mypage(monkeypatch, tmp_path):
    release_db = tmp_path / "pybo.db"
    release_db.write_bytes((Path(__file__).parents[1] / "pybo.db").read_bytes())
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{release_db}")

    import config

    importlib.reload(config)
    from pybo import create_app

    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()
    with client.session_transaction() as session:
        session["user_id"] = 1

    response = client.get("/film/mypage")

    assert response.status_code == 200
    assert b"OperationalError" not in response.data
