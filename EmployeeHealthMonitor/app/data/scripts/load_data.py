import csv
import os
import datetime
from app import create_app
from app.extensions import db
from app.apps.health.models import HealthData

def load_csv(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл {filepath} не найден.")

    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        records = []
        for idx, row in enumerate(reader, start=1):
            try:
                record = HealthData(
                    employee_id=int(row['employee_id']),
                    date=datetime.datetime.strptime(row['date'], "%Y-%m-%d").date(),
                    heart_rate=int(row['heart_rate']) if row.get('heart_rate') else None,
                    systolic=int(row['systolic']) if row.get('systolic') else None,
                    diastolic=int(row['diastolic']) if row.get('diastolic') else None,
                    steps=int(row['steps']) if row.get('steps') else None
                )
                records.append(record)
            except Exception as e:
                print(f" Ошибка в строке {idx}: {e}")

        if records:
            db.session.bulk_save_objects(records)
            db.session.commit()
            print(f"Загружено {len(records)} записей из {filepath}.")
        else:
            print(" Нет валидных данных для загрузки!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        load_csv('health_data.csv')
