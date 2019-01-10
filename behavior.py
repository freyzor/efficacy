from score import BehaviorScore


def calculate_consideration_score(input_broker, context, consideration, compensation_factor):
    score = consideration.score(input_broker, context)
    value = score.final_score
    score.final_score = value + value*compensation_factor - value**2*compensation_factor
    return score


class Behavior:
    def __init__(self, name, considerations=None):
        self.name = name
        self.considerations = considerations or []
        self.weight = 1.0
        self.action = None

    def score(self, input_broker, context):
        compensation_factor = self.get_compensation_factor()
        result = self.weight
        behavior_score = BehaviorScore(initial_weight=self.weight)

        for consideration in self.considerations:
            score = calculate_consideration_score(input_broker, context, consideration, compensation_factor)
            result *= score.final_score
            behavior_score.add_consideration_score(consideration, score)

        behavior_score.final_score = result
        return behavior_score

    def get_compensation_factor(self):
        return 1.0 - (1.0 / len(self.considerations))


class BehaviorSet:
    def __init__(self, name):
        self.name = name
        self.enabled_behaviors = set()
