# utils/normalizers.py
from config.constants import MAX_POLLUTION, MAX_COUNTRIES, MAX_INJURY_RATE

def normalize_gender_ratio(value):
    """Normalize gender ratio where 1:1 is perfect"""
    return max(0, 1 - abs(value - 1))

def normalize_pollution(value):
    """Normalize pollution where lower is better"""
    return max(0, 1 - value / MAX_POLLUTION)

def normalize_countries(value):
    """Normalize number of countries"""
    return min(max(0, value / MAX_COUNTRIES), 1)

def normalize_youth_appeal(value):
    """Normalize youth appeal percentage"""
    return value / 100

def normalize_injury_rate(value):
    """Normalize injury rate where lower is better"""
    return max(0, 1 - value / MAX_INJURY_RATE)