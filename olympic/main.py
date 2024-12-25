# main.py
from ahp.sport_analyzer import SportAnalyzer


def main():
    # Create analyzer
    analyzer = SportAnalyzer()

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

    # Add all sports
    for sport_data in sports_data:
        analyzer.add_sport(**sport_data)

    # Generate and print report
    print(analyzer.get_detailed_report())


if __name__ == "__main__":
    main()