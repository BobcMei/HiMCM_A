# ahp/calculator.py
import numpy as np
import warnings
from config.constants import (COMPARISON_MATRIX, CRITERIA)
from utils.normalizers import (
    normalize_gender_ratio,
    normalize_pollution,
    normalize_countries,
    normalize_youth_appeal,
    normalize_injury_rate
)


class AHPCalculator:
    def __init__(self):
        # Random Index values for matrices size 1 to 10
        self.RI = (0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49)
        # Get comparison matrix from constants
        self.criteria = np.array(COMPARISON_MATRIX)
        self.num_criteria = self.criteria.shape[0]
        self.weights = self._calculate_weights()

    def _calculate_weights(self):
        """Calculate weights using eigenvector method"""
        max_eigen, CR, weights = self.cal_weights(self.criteria)
        print(
            f'Criteria Layer: Max eigenvalue={max_eigen:.5f}, CR={CR:.5f}, Check {"Passed" if CR < 0.1 else "Failed"}')
        return weights

    def cal_weights(self, input_matrix):
        """Calculate weights for a given comparison matrix"""
        input_matrix = np.array(input_matrix)
        n, n1 = input_matrix.shape
        assert n == n1, 'Matrix must be square'

        # Check if matrix is reciprocal
        for i in range(n):
            for j in range(n):
                if np.abs(input_matrix[i, j] * input_matrix[j, i] - 1) > 1e-7:
                    raise ValueError('Matrix is not reciprocal')

        # Calculate eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(input_matrix)

        # Find largest eigenvalue and its eigenvector
        max_idx = np.argmax(eigenvalues)
        max_eigen = eigenvalues[max_idx].real
        eigen = eigenvectors[:, max_idx].real
        eigen = eigen / eigen.sum()  # Normalize eigenvector

        # Calculate consistency ratio
        if n > 9:
            CR = None
            warnings.warn('Cannot check consistency for n > 9')
        else:
            CI = (max_eigen - n) / (n - 1)
            CR = CI / self.RI[n - 1]
        return max_eigen, CR, eigen

    def normalize_values(self, values):
        """Normalize raw values to 0-1 scale"""
        return {
            'gender_ratio': normalize_gender_ratio(values['gender_ratio']),
            'pollution': normalize_pollution(values['pollution']),
            'covered_country': normalize_countries(values['covered_country']),
            'youth_appeal': normalize_youth_appeal(values['youth_appeal']),
            'injury_rate': normalize_injury_rate(values['injury_rate'])
        }

    def calculate_score(self, values):
        """Calculate final score using weights and normalized values"""
        normalized = self.normalize_values(values)
        score = sum(self.weights[i] * normalized[criterion]
                    for i, criterion in enumerate(CRITERIA))
        return score, normalized