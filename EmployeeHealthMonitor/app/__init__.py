# app/__init__.py

import os
from flask import Flask, render_template
from .config.settings import Config
from .extensions import db, ma, login_manager, celery
from datetime import datetime

# Относительные импорты Blueprint-ов и модели User
# app/__init__.py

from .apps.accounts.urls import accounts_bp
from .apps.employees.urls import employees_bp
from .apps.health.urls import health_bp
from .apps.reports.urls import reports_bp
from .apps.analytics.urls import analytics_bp



from app.apps.accounts.models import User
from werkzeug.security import generate_password_hash

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

    @app.context_processor
    def inject_datetime():
        return dict(datetime=datetime)

    # Инициализация расширений
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    celery.conf.update(app.config)


    with app.app_context():
        db.create_all()
        
        # Дополнительно: создание первого админа если нужно
        if not User.query.filter_by(is_admin=True).first():
            admin = User(
                last_name='Admin',
                first_name='System',
                email='admin@example.com',
                password_hash=generate_password_hash('admin'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            
    # Куда редиректить при @login_required
    login_manager.login_view = 'accounts.auth'

    # Как загружать current_user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Домашняя страница
    @app.route('/')
    def index():
        return render_template('login.html')

    # Регистрация Blueprints
    app.register_blueprint(accounts_bp,   url_prefix='/accounts')
    app.register_blueprint(employees_bp,  url_prefix='/employees')
    app.register_blueprint(health_bp,     url_prefix='/health')
    app.register_blueprint(reports_bp,    url_prefix='/reports')
    app.register_blueprint(analytics_bp,  url_prefix='/analytics')

    return app
