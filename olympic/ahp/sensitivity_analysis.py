# ahp/sensitivity_analysis.py
import numpy as np
from config.constants import CRITERIA

class SensitivityAnalysis:
    def __init__(self, calculator):
        self.calculator = calculator
        self.original_weights = calculator.weights.copy()

    def weight_sensitivity(self, sport, weight_changes=None):
        """Test how changes in criteria weights affect final score"""
        if weight_changes is None:
            weight_changes = [-0.2, -0.1, 0.1, 0.2]  # Default 20% changes

        results = {}
        original_score, _ = self.calculator.calculate_score(sport.values)

        for criterion_idx, criterion in enumerate(CRITERIA):
            criterion_results = []
            for change in weight_changes:
                # Modify one weight
                new_weights = self.original_weights.copy()
                new_weights[criterion_idx] *= (1 + change)
                # Renormalize weights
                new_weights = new_weights / np.sum(new_weights)

                # Calculate new score
                temp_weights = self.calculator.weights.copy()
                self.calculator.weights = new_weights
                new_score, _ = self.calculator.calculate_score(sport.values)
                self.calculator.weights = temp_weights

                criterion_results.append({
                    'change': f"{change:+.1%}",
                    'score': new_score,
                    'difference': new_score - original_score
                })
            results[criterion] = criterion_results

        return results, original_score

    def value_sensitivity(self, sport, value_changes=None):
        """Test how changes in sport values affect final score"""
        if value_changes is None:
            value_changes = [-0.2, -0.1, 0.1, 0.2]  # Default 20% changes

        results = {}
        original_values = sport.values.copy()
        original_score, _ = self.calculator.calculate_score(original_values)

        for criterion in CRITERIA:
            criterion_results = []
            for change in value_changes:
                # Modify one value
                new_values = original_values.copy()
                new_values[criterion] *= (1 + change)

                # Calculate new score
                new_score, _ = self.calculator.calculate_score(new_values)
                criterion_results.append({
                    'change': f"{change:+.1%}",
                    'score': new_score,
                    'difference': new_score - original_score
                })
            results[criterion] = criterion_results

        return results, original_score

    def criterion_removal_test(self, sport):
        """Test score changes when removing each criterion"""
        results = {}
        original_score, _ = self.calculator.calculate_score(sport.values)

        for criterion_idx, criterion in enumerate(CRITERIA):
            # Create new weights excluding one criterion
            new_weights = np.delete(self.original_weights.copy(), criterion_idx)
            new_weights = new_weights / np.sum(new_weights)

            # Create new values dictionary without this criterion
            new_values = sport.values.copy()
            del new_values[criterion]

            # Temporarily modify calculator weights
            temp_weights = self.calculator.weights.copy()
            self.calculator.weights = new_weights

            # Calculate normalized values manually
            normalized_values = {}
            for crit in new_values:
                if crit == 'gender_ratio':
                    normalized_values[crit] = max(0, 1 - abs(new_values[crit] - 1))
                elif crit == 'pollution':
                    normalized_values[crit] = max(0, 1 - new_values[crit] / 50)  # MAX_POLLUTION = 50
                elif crit == 'covered_country':
                    normalized_values[crit] = min(max(0, new_values[crit] / 200), 1)  # MAX_COUNTRIES = 200
                elif crit == 'youth_appeal':
                    normalized_values[crit] = new_values[crit] / 100
                elif crit == 'injury_rate':
                    normalized_values[crit] = max(0, 1 - new_values[crit] / 10)  # MAX_INJURY_RATE = 10

            # Calculate new score manually
            new_score = sum(new_weights[i] * normalized_values[crit]
                          for i, crit in enumerate(normalized_values))

            # Restore original weights
            self.calculator.weights = temp_weights

            results[criterion] = {
                'score': new_score,
                'difference': new_score - original_score
            }

        return results, original_score

    def generate_report(self, sport):
        """Generate comprehensive sensitivity analysis report"""
        report = "SENSITIVITY ANALYSIS REPORT\n"
        report += "=" * 50 + "\n\n"

        # Weight sensitivity analysis
        report += "1. WEIGHT SENSITIVITY ANALYSIS\n"
        report += "-" * 30 + "\n"
        weight_results, original_score = self.weight_sensitivity(sport)
        report += f"Original Score: {original_score:.4f}\n\n"

        for criterion, changes in weight_results.items():
            report += f"\n{criterion}:\n"
            for change in changes:
                report += (f"  {change['change']:>6} weight change: "
                         f"Score = {change['score']:.4f} "
                         f"(Δ: {change['difference']:+.4f})\n")

        # Value sensitivity analysis
        report += "\n2. VALUE SENSITIVITY ANALYSIS\n"
        report += "-" * 30 + "\n"
        value_results, _ = self.value_sensitivity(sport)

        for criterion, changes in value_results.items():
            report += f"\n{criterion}:\n"
            for change in changes:
                report += (f"  {change['change']:>6} value change: "
                         f"Score = {change['score']:.4f} "
                         f"(Δ: {change['difference']:+.4f})\n")

        # Criterion removal analysis
        report += "\n3. CRITERION REMOVAL ANALYSIS\n"
        report += "-" * 30 + "\n"
        removal_results, _ = self.criterion_removal_test(sport)

        for criterion, result in removal_results.items():
            report += (f"Without {criterion}: "
                     f"Score = {result['score']:.4f} "
                     f"(Δ: {result['difference']:+.4f})\n")

        return report