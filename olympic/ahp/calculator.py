# ahp/calculator.py
import numpy as np
from config.constants import CRITERIA, COMPARISON_MATRIX
from utils.normalizers import *


class AHPCalculator:
    def __init__(self):
        self.weights = self._calculate_weights()
#用神秘的eigenvalue算weights
    def _calculate_weights(self):
        matrix = np.array(COMPARISON_MATRIX)
        eigenvals, eigenvects = np.linalg.eig(matrix)
        principal_eigenval_idx = np.argmax(eigenvals.real)
        principal_eigenvect = eigenvects[:, principal_eigenval_idx].real
        return principal_eigenvect / np.sum(principal_eigenvect)
#这里的values来自sport，引用normalizers的function
    def normalize_values(self, values):
        return {
            'gender_ratio': normalize_gender_ratio(values['gender_ratio']),
            'pollution': normalize_pollution(values['pollution']),
            'covered_country': normalize_countries(values['covered_country']),
            'youth_appeal': normalize_youth_appeal(values['youth_appeal']),
            'injury_rate': normalize_injury_rate(values['injury_rate'])
        }

    def calculate_score(self, values):
        normalized = self.normalize_values(values)
        score = sum(self.weights[i] * normalized[criterion]
                    for i, criterion in enumerate(CRITERIA))
        return score, normalized