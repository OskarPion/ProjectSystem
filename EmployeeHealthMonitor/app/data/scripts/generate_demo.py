from app import create_app
from app.extensions import db
from app.apps.accounts.models import User
from app.apps.employees.models import Employee
from app.apps.health.models import HealthData
from app.apps.reports.models import Report
from app.core.models import Disease   # <--- ДОБАВИТЬ
from faker import Faker
import random
import datetime

fake = Faker()

def generate_demo():
    app = create_app()

    with app.app_context():
        print('Старт генерации демо-данных...')

        # 1. Очистить таблицы
        print(' Очищаем старые данные...')
        Report.query.delete()
        Employee.query.delete()
        Disease.query.delete()
        User.query.delete()
        db.session.commit()

        # 2. Генерация пользователей
        print('Генерируем пользователей...')
        users = []
        for _ in range(20):
            user = User(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password_hash=fake.password(length=12)
            )
            users.append(user)
            db.session.add(user)

        db.session.commit()
        print(f"Создано {len(users)} пользователей.")

        # 3. Генерация сотрудников
        print('Генерируем сотрудников...')
        employees = []
        for user in users:
            employee = Employee(
                user_id=user.id,
                name=fake.name(),
                position=fake.job(),
                hire_date=fake.date_between(start_date='-10y', end_date='today')
            )
            employees.append(employee)
            db.session.add(employee)

        db.session.commit()
        print(f"Создано {len(employees)} сотрудников.")

        # 4. Генерация болезней
        print('Генерируем болезни...')
        diseases = []
        disease_names = set()
        while len(disease_names) < 10:
            disease_names.add(fake.word().capitalize())

        for name in disease_names:
            disease = Disease(
                name=name,
                description=fake.text(max_nb_chars=200)
            )
            diseases.append(disease)
            db.session.add(disease)

        db.session.commit()
        print(f"Создано {len(diseases)} заболеваний.")

        # 5. Генерация отчётов
        print('Генерируем отчёты по заболеваниям...')
        for _ in range(50):
            report = Report(
                employee_id=fake.random_element(elements=[e.id for e in employees]),
                disease_id=fake.random_element(elements=[d.id for d in diseases]),
                date=fake.date_between(start_date='-1y', end_date='today')
            )
            db.session.add(report)

        db.session.commit()
        print(f"Создано 50 отчётов.")

        print('Демо-данные успешно сгенерированы!')

if __name__ == '__main__':
    generate_demo()