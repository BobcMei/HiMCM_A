# Constants for normalization
MAX_POLLUTION = 50  # tonnes
MAX_COUNTRIES = 200
MAX_INJURY_RATE = 10  # percent

# Criteria names
CRITERIA = ['gender_ratio', 'pollution', 'covered_country', 'youth_appeal', 'injury_rate']

# Pairwise comparison matrix
COMPARISON_MATRIX = [
    [1, 3, 1/3, 2, 1/7],    # Gender ratio
    [1/3, 1, 1/5, 1/2, 1/9], # Pollution
    [3, 5, 1, 3, 1/3],       # Covered country
    [1/2, 2, 1/3, 1, 1/5],   # Youth appeal
    [7, 9, 3, 5, 1]          # Athlete injury rate
]