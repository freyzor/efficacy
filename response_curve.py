import math

from lazy import repr_dict_object
from mathutil import clamp

MATH_2PI = 2.0 * math.pi
MATH_SQRT_2PI = MATH_2PI ** 0.5


class ResponseCurve(object):
    def __init__(self, x_offset=0.0, y_offset=0.0):
        self.x_offset = x_offset
        self.y_offset = y_offset

    def compute_value(self, x):
        return 0.0

    def __repr__(self):
        return repr_dict_object(self)


class ScaledResponseCurve(ResponseCurve):
    def __init__(self, x_offset=0.0, y_offset=0.0, x_scale=1.0, y_scale=1.0):
        super(ScaledResponseCurve, self).__init__(x_offset, y_offset)
        self.x_scale = x_scale
        self.y_scale = y_scale


class LinearCurve(ResponseCurve):
    def __init__(self, x_offset=0.0, y_offset=0.0, slope=1.0):
        super(LinearCurve, self).__init__(x_offset, y_offset)
        self.slope = slope

    def compute_value(self, x):
        value = (self.slope * (x - self.x_offset)) + self.y_offset
        return sanitize_value(value)


class LogitCurve(ScaledResponseCurve):
    """
    https://en.wikipedia.org/wiki/Logit
    goes from -inf to inf but I have clamped the output to a 'reasonable' range
    """

    def compute_value(self, x):
        x0 = clamp(x * self.y_scale - self.x_offset, 0.0000001, 0.9999999)
        value = self.y_scale * math.log(x0 / (1.0 - x0)) / 5.0 + 0.5 + self.y_offset
        return sanitize_value(value)


class SineCurve(ResponseCurve):
    def __init__(self, x_offset=0.0, y_offset=0.0, amplitude=1.0, frequency_scale=1.0):
        super(SineCurve, self).__init__(x_offset, y_offset)
        self.amplitude = amplitude
        self.frequency_scale = frequency_scale

    def compute_value(self, x):
        x0 = (x - self.x_offset)
        value = 0.5 * self.amplitude * -math.cos(MATH_2PI * x0 * self.frequency_scale) + 0.5 + self.y_offset
        return sanitize_value(value)


class PolynomialCurve(ResponseCurve):
    def __init__(self, x_offset=0.0, y_offset=0.0, y_scale=1.0, exponent=2.0):
        super(PolynomialCurve, self).__init__(x_offset=x_offset, y_offset=y_offset)
        self.y_scale = y_scale
        self.exponent = exponent

    def compute_value(self, x):
        value = (self.y_scale * math.pow(x - self.x_offset, self.exponent)) + self.y_offset
        return sanitize_value(value)


class LogisticCurve(ScaledResponseCurve):
    """
    https://en.wikipedia.org/wiki/Generalised_logistic_function
    y_scale: amplitude, K
    x_scale: compression on the x axis

    crossover: is the value of x where the function goes from low to high
    slope: is the steepness of the curve
    """

    def __init__(self, x_offset=0.0, y_offset=0.0, x_scale=1.0, y_scale=1.0, slope=0.5, crossover=0.5):
        super(LogisticCurve, self).__init__(x_offset, y_offset, x_scale, y_scale)
        if slope is not None and crossover is not None:
            scaling = 1.0 / crossover
            self.x_scale = slope * scaling
            self.x_offset = crossover * slope * scaling

    def compute_value(self, x):
        x0 = self.x_scale * x - self.x_offset
        value = (self.y_scale * 1 / (1 + math.exp(- x0))) + self.y_offset
        return sanitize_value(value)


class NormalCurve(ResponseCurve):
    """
    Normal distribution curve
    mean: mu the expected value
    std_dev: sigma the standard deviation
    y_scale: scale the whole of the y axis (output/amplitude)
    """

    def __init__(self, x_offset=0.0, y_offset=0.0, y_scale=1.0, mean=0.0, std_dev=1.0, normalize=True):
        super(NormalCurve, self).__init__(x_offset=x_offset, y_offset=y_offset)
        self.mean = mean
        self.std_dev = std_dev
        if normalize:
            peak = bell_curve(0.0, 0.0, std_dev)
            self.y_scale = 1.0 / peak * y_scale

        else:
            self.y_scale = y_scale

    def compute_value(self, x):
        value = self.y_scale * bell_curve((x - self.x_offset), self.mean, self.std_dev) - self.y_offset
        return sanitize_value(value)


def bell_curve(x, mean, std_dev):
    return (1.0 / (std_dev * MATH_SQRT_2PI)) * math.exp(-((x - mean) ** 2 / (2.0 * std_dev ** 2)))


def sanitize_value(x):
    if math.isinf(x):
        return 0.0

    if math.isnan(x):
        return 0.0

    if x < 0.0:
        return 0.0

    if x > 1.0:
        return 1.0

    return x


RESPONSE_CURVE_MAP = {
    "linear": LinearCurve,
    "polynomial": PolynomialCurve,
    "logistic": LogisticCurve,
    "logit": LogitCurve,
    "normal": NormalCurve,
    "sine": SineCurve,
}


HIGH_LOW_SINE_CURVE = SineCurve(frequency_scale=0.5, x_offset=1)
LOW_HIGH_SINE_CURVE = SineCurve(frequency_scale=0.5)
