import unittest
import mock
import response_curve as curves
from behavior import Behavior
from consideration import Consideration
from context import Context
from input_parameter import InputBroker

CONSIDERATION_1 = mock.sentinel.CONSIDERATION_1
CONSIDERATION_2 = mock.sentinel.CONSIDERATION_2


class MockInputBroker(InputBroker):
    def __init__(self, input_map):
        self.input_map = input_map

    def get_input_value(self, consideration, context):
        return self.input_map[consideration.name]


class UtilityTestCase(unittest.TestCase):
    def test_two_considerations_are_combined_as_expected(self):
        val_1 = 0.8
        val_2 = 0.5
        input_broker = MockInputBroker({
            CONSIDERATION_1: 0.8,
            CONSIDERATION_2: 0.5,
        })
        consideration_1 = Consideration(
            CONSIDERATION_1,
            curves.LinearCurve(x_offset=0.0, y_offset=0.0, slope=1.0),
            min_value=0.0,
            max_value=1.0,
        )
        consideration_2 = Consideration(
            CONSIDERATION_2,
            curves.LinearCurve(x_offset=0.0, y_offset=0.0, slope=1.0),
            min_value=0.0,
            max_value=1.0,
        )
        behavior = Behavior("test")
        behavior.considerations.append(consideration_1)
        behavior.considerations.append(consideration_2)
        f = behavior.get_compensation_factor()
        score = behavior.score(input_broker, Context)
        expected = (val_1 + val_1*f - val_1**2*f) * (val_2 + val_2*f - val_2**2*f)
        self.assertEqual(expected, score.final_score)

    def test_simple_linear_behavior_returns_input_value_as_score(self):
        val_1 = 0.8
        input_broker = MockInputBroker({
            CONSIDERATION_1: 0.8,
        })
        consideration_1 = Consideration(
            CONSIDERATION_1,
            curves.LinearCurve(x_offset=0.0, y_offset=0.0, slope=1.0),
            min_value=0.0,
            max_value=1.0,
        )
        behavior = Behavior("test")
        behavior.considerations.append(consideration_1)
        score = behavior.score(input_broker, Context)
        expected = val_1
        self.assertEqual(expected, score.final_score)

    def test_LinearCurve_zero_params_generate_zero_result(self):
        curve = curves.LinearCurve(x_offset=0.0, y_offset=0.0, slope=0.0)
        self.assertEqual(0.0, curve.compute_value(0))
        self.assertEqual(0.0, curve.compute_value(1.0))

    def test_LinearCurve_with_slope_1_generate_line_from_0_to_1(self):
        curve = curves.LinearCurve(x_offset=0.0, y_offset=0.0, slope=1.0)
        self.assertEqual(0.0, curve.compute_value(0))
        self.assertEqual(1.0, curve.compute_value(1.0))

    def test_NormalCurve_normalized_mean_1_std_dev_1_value_at_1_is_1(self):
        curve = curves.NormalCurve(x_offset=0.0, y_offset=0.0, mean=1.0, std_dev=1.0, y_scale=1.0, normalize=True)
        self.assertEqual(1.0, curve.compute_value(1.0))

    def test_NormalCurve_normalized_mean_1_std_dev_0_1_value_at_1_is_1(self):
        curve = curves.NormalCurve(x_offset=0.0, y_offset=0.0, mean=1.0, std_dev=0.1, y_scale=1.0, normalize=True)
        self.assertAlmostEqual(0.0, curve.compute_value(0.0))


if __name__ == '__main__':
    unittest.main()
