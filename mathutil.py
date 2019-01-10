
def clamp(value, min_value=0.0, max_value=1.0):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value

    return value


def normalize_value(value, min_value, max_value):
    value = clamp(value, min_value, max_value)
    return (value - min_value) / (max_value - min_value)
