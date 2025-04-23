# apps/health/models.py
from django.db import models
from django.conf import settings


class Disease(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icd_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class HealthRecord(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='health_records'
    )
    record_date = models.DateField()
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    bmi = models.FloatField(blank=True)
    systolic_bp = models.IntegerField(blank=True, null=True)
    diastolic_bp = models.IntegerField(blank=True, null=True)
    total_cholesterol = models.FloatField(blank=True, null=True)
    fasting_glucose = models.FloatField(blank=True, null=True)
    disease = models.ForeignKey(
        Disease,
        on_delete=models.SET_NULL,
        related_name='records',
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-record_date']
        unique_together = ('employee', 'record_date')

    def save(self, *args, **kwargs):
        # Calculate BMI if not provided
        if not self.bmi and self.height_cm and self.weight_kg:
            h_m = self.height_cm / 100
            self.bmi = self.weight_kg / (h_m * h_m)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.record_date}"
