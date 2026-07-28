import importlib


def test_config_uses_database_url_from_environment(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:////tmp/filmatique-test.db")
    import config

    reloaded = importlib.reload(config)

    assert reloaded.SQLALCHEMY_DATABASE_URI == "sqlite:////tmp/filmatique-test.db"


def test_create_app_has_debug_disabled(monkeypatch):
    monkeypatch.setenv("FLASK_DEBUG", "0")
    from pybo import create_app

    app = create_app()

    assert app.debug is False
