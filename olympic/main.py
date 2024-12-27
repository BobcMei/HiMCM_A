# main.py
from ahp.sport_analyzer import SportAnalyzer
from models.sport import Sport
from config.sport_data import TASK3_SPORTS

def main():
    # Create analyzer
    analyzer = SportAnalyzer()

    # Add all sports from Task 3 data
    for sport_name, sport_data in TASK3_SPORTS.items():
        # Create Sport object first
        sport = Sport(name=sport_name, data=sport_data)
        # Add to analyzer
        analyzer.sports[sport.name] = sport

    # Generate and print overall report
    print(analyzer.get_detailed_report())

if __name__ == "__main__":
    main()