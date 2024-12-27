# config/constants.py

# Main criteria comparison matrix (6x6 matrix)
COMPARISON_MATRIX = [
    [1.0, 2.0, 3.0, 1.0, 2.0, 0.5],  # Pop
    [0.5, 1.0, 2.0, 0.5, 1.0, 0.3333],  # Gender
    [0.3333, 0.5, 1.0, 0.3333, 0.5, 0.25],  # Sustain
    [1.0, 2.0, 3.0, 1.0, 2.0, 0.5],  # Inclus
    [0.5, 1.0, 2.0, 0.5, 1.0, 0.3333],  # Relev
    [2.0, 3.0, 4.0, 2.0, 3.0, 1.0]  # Safety
]

# Sub-criteria matrices
SUBCRITERIA_MATRICES = {
    'popularity_accessibility': [[1, 1], [1, 1]],
    'inclusivity': [
        [1, 2],
        [0.5, 1]
    ],
    'relevance_innovation': [[1, 2], [0.5, 1]],
    'safety_fairplay': [
        [1, 2, 3],
        [0.5, 1, 2],
        [0.3333, 0.5, 1]
    ]
}

# Criteria names
CRITERIA = [
    'popularity_accessibility',
    'gender_equity',
    'sustainability',
    'inclusivity',
    'relevance_innovation',
    'safety_fairplay'
]