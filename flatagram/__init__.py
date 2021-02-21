from flask import Flask, render_template
from flask_migrate import Migrate

import os

migrate = Migrate()


def page_not_found(error):
    return render_template('404.html'), 404


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    from .models import db
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # Blueprint
    from .views import main_views, post_views, comment_views, auth_views, explore_views, user_views, like_views, dm_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(post_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(explore_views.bp)
    app.register_blueprint(user_views.bp)
    app.register_blueprint(like_views.bp)
    app.register_blueprint(dm_views.bp)

    # Error Page
    app.register_error_handler(404, page_not_found)
    return app
