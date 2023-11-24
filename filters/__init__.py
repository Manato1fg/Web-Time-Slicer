from .y import Y
from .x import X
from .t import T
from .yaw import Yaw
from .pitch import Pitch
from .roll import Roll

def get_all_filter_names():
    return [Y.get_name(), X.get_name(), T.get_name(), Yaw.get_name(), Pitch.get_name(), Roll.get_name()]

def get_filter_by_name(name: str):
    if name == Y.get_name():
        return Y()
    elif name == X.get_name():
        return X()
    elif name == T.get_name():
        return T()
    elif name == Yaw.get_name():
        return Yaw()
    elif name == Pitch.get_name():
        return Pitch()
    elif name == Roll.get_name():
        return Roll()
    else:
        raise Exception(f"Filter {name} not found")