from mathutil import normalize_value
from response_curve import LinearCurve
from response_curve import ResponseCurve
from score import Score


class Consideration:

    def __init__(self, name, curve=LinearCurve(), min_value=0.0, max_value=1.0, **kwargs):
        self.name = name
        self.curve = curve  # type: ResponseCurve
        self.min_value = min_value
        self.max_value = max_value
        # we can pass in arbitrary parameters in but they have to match the input type being requested
        self.__dict__.update(kwargs)

    def score(self, input_broker, context):
        input_raw_value = input_broker.get_input_value(self, context)
        input_value = normalize_value(input_raw_value, self.min_value, self.max_value)
        final_score = self.curve.compute_value(input_value)
        print("consideration:", self.name, self.curve, "raw", input_raw_value, "norm", input_value, "final", final_score, "max", self.max_value)
        score = Score(
            input_raw_value=input_raw_value,
            input_value=input_value,
            final_score=final_score
        )
        return score

