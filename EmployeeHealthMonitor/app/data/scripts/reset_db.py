# app/data/scripts/reset_db.py

from app import create_app
from app.extensions import db

def reset_database():
    app = create_app()
    print('🔵 DATABASE_URI:', app.config['SQLALCHEMY_DATABASE_URI'])
    import os
    print('🔵 Текущая папка:', os.getcwd())
    with app.app_context():
        print("🚀 Удаляем старые таблицы...")
        db.drop_all()
        print("✅ Старые таблицы удалены.")
        db.create_all()
        print("✅ Новые таблицы созданы!")

if __name__ == '__main__':
    reset_database()
