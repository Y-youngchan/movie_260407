from flask import Flask


def create_app():
    app = Flask(__name__)
    # app.config.from_object('config')

    #블루프린트 등록
    from .views import main_views
    app.register_blueprint(main_views.bp)
    # app.register_blueprint(auth_views.bp)
    # app.register_blueprint(question_views.bp)

    return app