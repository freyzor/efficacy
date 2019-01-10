class InputBroker:
    """Abstract class responsible for providing raw values when considering scores"""
    def get_input_value(self, consideration, context):
        raise NotImplementedError()
