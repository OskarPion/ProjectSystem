# apps/analytics/ml_models.py
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from django.conf import settings


def load_health_data(queryset):
    """
    Принимает QuerySet HealthRecord, возвращает DataFrame
    """
    df = pd.DataFrame.from_records(
        queryset.values(
            'employee_id', 'bmi', 'systolic_bp', 'diastolic_bp',
            'total_cholesterol', 'fasting_glucose', 'disease'
        )
    )
    # Предобработка
    df = df.dropna(subset=['bmi', 'systolic_bp', 'fasting_glucose'])
    return df


class DiabetesRiskModel:
    """
    Простейшая модель для прогнозирования риска диабета
    """
    def __init__(self):
        self.pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
            ('clf', LogisticRegression())
        ])

    def train(self, df: pd.DataFrame):
        X = df[['bmi', 'systolic_bp', 'total_cholesterol', 'fasting_glucose']]
        y = (df['disease'] == Disease.objects.get(name='Diabetes').id).astype(int)
        self.pipeline.fit(X, y)

    def predict_proba(self, df: pd.DataFrame):
        X = df[['bmi', 'systolic_bp', 'total_cholesterol', 'fasting_glucose']]
        return self.pipeline.predict_proba(X)[:, 1]

    def save_model(self, path):
        import joblib
        joblib.dump(self.pipeline, path)

    def load_model(self, path):
        import joblib
        self.pipeline = joblib.load(path)
