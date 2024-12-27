# ahp/sport_analyzer.py
from models.sport import Sport
from ahp.calculator import AHPCalculator


class SportAnalyzer:
    def __init__(self):
        self.calculator = AHPCalculator()
        self.sports = {}

    def add_sport(self, name, gender_ratio, pollution, covered_country, youth_appeal, injury_rate):
        sport = Sport(name, gender_ratio, pollution, covered_country, youth_appeal, injury_rate)
        self.sports[name] = sport
        return sport

    def analyze_all(self):
        """Analyze all sports and sort by score"""
        for sport in self.sports.values():
            score, normalized = self.calculator.calculate_score(sport.values)
            sport.set_results(score, normalized)

        return sorted(self.sports.values(), key=lambda x: x.score, reverse=True)

    def get_detailed_report(self):
        """Generate detailed report for all sports"""
        analyzed_sports = self.analyze_all()
        report = "Olympic Sports Analysis Report\n"
        report += "=" * 50 + "\n\n"

        for rank, sport in enumerate(analyzed_sports, 1):
            report += f"Rank {rank}: {sport.name}\n"
            report += f"Overall Score: {sport.score:.4f}\n"
            report += "\nDetailed Criteria Scores:\n"
            for criterion, value in sport.normalized_values.items():
                report += f"- {criterion}: {value:.4f}\n"

            # Add 75+ countries information
            report += f"75+ Countries Requirement: {'Met' if sport.values['countries_75plus'] else 'Not Met'}\n"

            report += "-" * 30 + "\n\n"

        return report