from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import config
from pybo.services.tmdb_service import save_movies

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')


    #ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    with app.app_context():
        from pybo.models import Movie

    #블루프린트 등록

    from .views import main_views, auth_views, film_views, cs_views, store_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(film_views.bp)
    app.register_blueprint(cs_views.bp)
    app.register_blueprint(store_views.bp)

    return app