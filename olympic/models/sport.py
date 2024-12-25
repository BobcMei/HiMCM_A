# models/sport.py
class Sport:
    # 给每个sport的信息归类
    def __init__(self, name, gender_ratio, pollution, covered_country, youth_appeal, injury_rate):
        self.name = name
        self.values = {
            'gender_ratio': gender_ratio,
            'pollution': pollution,
            'covered_country': covered_country,
            'youth_appeal': youth_appeal,
            'injury_rate': injury_rate
        }
        self.score = None
        self.normalized_values = None

    def set_results(self, score, normalized_values):
        self.score = score
        self.normalized_values = normalized_values

    def __str__(self):
        return f"{self.name} (Score: {self.score:.4f if self.score else 'Not calculated'})"