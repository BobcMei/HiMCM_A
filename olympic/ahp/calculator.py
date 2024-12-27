# ahp/calculator.py
import numpy as np
import warnings
from config.constants import COMPARISON_MATRIX, CRITERIA, SUBCRITERIA_MATRICES


class AHPCalculator:
    def __init__(self):
        # Random Index values for matrices size 1 to 10 (Saaty's values)
        self.RI = (0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49)
        # Get comparison matrix from constants
        self.criteria = np.array(COMPARISON_MATRIX, dtype=float)
        self.num_criteria = self.criteria.shape[0]
        self.weights = self._calculate_weights()
        # Calculate sub-criteria weights
        self.subcriteria_weights = self._calculate_subcriteria_weights()

    def _calculate_weights(self):
        """Calculate weights using eigenvector method"""
        max_eigen, CR, weights = self.cal_weights(self.criteria)
        if CR is not None:
            print(
                f'Criteria Layer: Max eigenvalue={max_eigen:.5f}, CR={CR:.5f}, '
                f'Check {"Passed" if CR < 0.1 else "Failed"}'
            )
        return weights

    def cal_weights(self, input_matrix):
        """Calculate weights using Saaty's eigenvector method"""
        try:
            input_matrix = np.array(input_matrix, dtype=float)
            n = input_matrix.shape[0]

            # Calculate eigenvalues and eigenvectors
            eigenvalues, eigenvectors = np.linalg.eig(input_matrix)

            # Find largest eigenvalue and its eigenvector
            max_idx = np.argmax(np.real(eigenvalues))
            max_eigen = np.real(eigenvalues[max_idx])
            eigen = np.real(eigenvectors[:, max_idx])
            eigen = eigen / np.sum(eigen)  # Normalize eigenvector

            # Calculate consistency ratio
            if n <= 2:
                CR = 0.0
            elif n > 9:
                CR = None
                warnings.warn('Cannot check consistency for n > 9')
            else:
                CI = (max_eigen - n) / (n - 1)
                CR = CI / self.RI[n - 1] if self.RI[n - 1] != 0 else 0.0

            return max_eigen, CR, eigen

        except Exception as e:
            print(f"Error in cal_weights: {e}")
            print(f"Input matrix: {input_matrix}")
            raise

    def _calculate_subcriteria_weights(self):
        """Calculate weights for all sub-criteria"""
        subcriteria_weights = {}

        for criterion, matrix in SUBCRITERIA_MATRICES.items():
            if matrix is not None and len(matrix) > 1:
                matrix_array = np.array(matrix, dtype=float)
                _, _, weights = self.cal_weights(matrix_array)
                subcriteria_weights[criterion] = weights
            else:
                subcriteria_weights[criterion] = np.array([1.0])

        return subcriteria_weights

    def _aggregate_subcriteria_scores(self, values, criterion):
        """Aggregate sub-criteria scores for a given criterion"""
        if criterion in ['gender_equity', 'sustainability']:
            return values[criterion]

        weights = self.subcriteria_weights.get(criterion)
        if weights is None:
            raise ValueError(f"No weights found for criterion: {criterion}")

        if criterion == 'popularity_accessibility':
            subcriteria_values = [values['popularity'], values['cost']]
        elif criterion == 'inclusivity':
            subcriteria_values = [
                values['cultural_diversity'],
                values['age_diversity']
            ]
        elif criterion == 'relevance_innovation':
            subcriteria_values = [values['youth_appeal'], values['tech_index']]
        elif criterion == 'safety_fairplay':
            subcriteria_values = [
                values['injury_rate'],
                values['doping'],
                values['safety_equipment']
            ]
        else:
            raise ValueError(f"Unknown criterion: {criterion}")

        return np.dot(weights, subcriteria_values)

    def calculate_score(self, values):
        """Calculate final score using weights and normalized values"""
        # Calculate scores for each main criterion
        main_scores = []
        for criterion in CRITERIA:
            criterion_score = self._aggregate_subcriteria_scores(values, criterion)
            main_scores.append(criterion_score)

        # Calculate final score using main criteria weights
        final_score = np.dot(main_scores, self.weights)

        # Return both final score and normalized values
        normalized_values = dict(zip(CRITERIA, main_scores))

        return final_score, normalized_values