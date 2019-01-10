
def repr_dict_object(obj):
    return "{}({})".format(obj.__class__.__name__, ", ".join(
        "{}={}".format(k, v) for k, v in obj.__dict__.items() if not k.startswith("__")))



