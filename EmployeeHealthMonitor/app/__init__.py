# app/__init__.py

import os
from flask import Flask, render_template
from .config.settings import Config
from .extensions import db, ma, login_manager, celery

# Относительные импорты Blueprint-ов и модели User
# app/__init__.py

from .apps.accounts.urls import accounts_bp
from .apps.employees.urls import employees_bp
from .apps.health.urls import health_bp
from .apps.reports.urls import reports_bp
from .apps.analytics.urls import analytics_bp


def create_app():
    # Путь до папки app/
    pkg_dir = os.path.abspath(os.path.dirname(__file__))
    # Указываем Flask, где лежат шаблоны и статика
    template_dir = os.path.join(pkg_dir, 'templates')
    static_dir   = os.path.join(pkg_dir, 'static')

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    celery.conf.update(app.config)

    # Куда редиректить при @login_required
    login_manager.login_view = 'accounts.login'

    # Как загружать current_user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Домашняя страница
    @app.route('/')
    def index():
        return render_template('index.html')

    # Регистрация Blueprints
    app.register_blueprint(accounts_bp,   url_prefix='/accounts')
    app.register_blueprint(employees_bp,  url_prefix='/employees')
    app.register_blueprint(health_bp,     url_prefix='/health')
    app.register_blueprint(reports_bp,    url_prefix='/reports')
    app.register_blueprint(analytics_bp,  url_prefix='/analytics')

    return app
