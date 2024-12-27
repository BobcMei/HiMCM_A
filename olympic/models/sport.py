# models/sport.py
class Sport:
    def __init__(self, name, data):
        """
        Initialize a Sport object with name and criteria values

        Args:
            name (str): Name of the sport
            data (dict): Dictionary containing all criteria values
        """
        self.name = name
        # Map the input data to the structure expected by calculator
        self.values = {
            # Direct criteria values
            'gender_equity': data['gender_ratio'],
            'sustainability': data['environmental'],

            # Sub-criteria values - these need to be available directly
            'popularity': data['popularity'],
            'cost': data['cost'],
            'cultural_diversity': data['cultural_diversity'],
            'age_diversity': data['age_diversity'],
            'countries_75plus': data['countries_75plus'],
            'youth_appeal': data['youth_appeal'],
            'tech_index': data['tech_index'],
            'injury_rate': data['injury_rate'],
            'doping': data['doping'],
            'safety_equipment': data['safety_equipment'],

            # Pre-calculate aggregated scores for criteria with sub-criteria
            'popularity_accessibility': (data['popularity'] + data['cost']) / 2,
            'inclusivity': (data['cultural_diversity'] + data['age_diversity'] + (
                1.0 if data['countries_75plus'] else 0.0)) / 3,
            'relevance_innovation': (data['youth_appeal'] + data['tech_index']) / 2,
            'safety_fairplay': (data['injury_rate'] + data['doping'] + data['safety_equipment']) / 3
        }
        self.score = None
        self.normalized_values = None

    def set_results(self, score, normalized_values):
        """Set analysis results"""
        self.score = score
        self.normalized_values = normalized_values

    def __str__(self):
        return f"{self.name} (Score: {self.score:.4f if self.score else 'Not calculated'})"