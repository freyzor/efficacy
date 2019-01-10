from lazy import repr_dict_object


class Score:
    def __init__(self, input_raw_value=0.0, input_value=0.0, final_score=0.0):
        self.input_raw_value = input_raw_value
        self.input_value = input_value
        self.final_score = final_score

    def __repr__(self):
        return repr_dict_object(self)


class BehaviorScore:
    def __init__(self, initial_weight):
        self.score_by_consideration = {}
        self.initial_weight = initial_weight
        self.final_score = 0.0

    def add_consideration_score(self, consideration, score):
        self.score_by_consideration[consideration] = score

    def __repr__(self):
        return repr_dict_object(self)
