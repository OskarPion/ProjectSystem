import datetime

def calculate_baseline(records):
    """Compute average heart rate baseline."""
    if not records:
        return 0
    return sum(r.heart_rate for r in records) / len(records)
