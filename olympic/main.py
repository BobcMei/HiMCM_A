# main.py
from ahp.sport_analyzer import SportAnalyzer
from ahp.sensitivity_analysis import SensitivityAnalysis
from models.sport import Sport


def main():
    # Create analyzer
    analyzer = SportAnalyzer()
    # Create sensitivity analysis
    sensitivity = SensitivityAnalysis(analyzer.calculator)

    # Example sports data
    sports_data = [
        {
            "name": "Basketball",
            "gender_ratio": 1.1,
            "pollution": 15,
            "covered_country": 150,
            "youth_appeal": 85,
            "injury_rate": 4
        },
        {
            "name": "Swimming",
            "gender_ratio": 1.0,
            "pollution": 10,
            "covered_country": 180,
            "youth_appeal": 70,
            "injury_rate": 2
        },
        {
            "name": "Skateboarding",
            "gender_ratio": 1.3,
            "pollution": 5,
            "covered_country": 90,
            "youth_appeal": 95,
            "injury_rate": 7
        }
    ]

    # Add all sports and analyze them
    for sport_data in sports_data:
        # Create Sport object first
        sport = Sport(
            name=sport_data["name"],
            gender_ratio=sport_data["gender_ratio"],
            pollution=sport_data["pollution"],
            covered_country=sport_data["covered_country"],
            youth_appeal=sport_data["youth_appeal"],
            injury_rate=sport_data["injury_rate"]
        )
        # Add to analyzer
        analyzer.sports[sport.name] = sport
        # Generate sensitivity report
        print(sensitivity.generate_report(sport))

    # Generate and print overall report
    print(analyzer.get_detailed_report())


if __name__ == "__main__":
    main()