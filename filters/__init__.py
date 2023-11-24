from .y import Y
from .x import X
from .t import T
from .yaw import Yaw
from .pitch import Pitch
from .roll import Roll
from .time_wave import TimeWave
from .sin import Sin
from .tile import Tile

def get_all_filter_names():
    return [
        Y.get_name(),
        X.get_name(),
        T.get_name(),
        Yaw.get_name(),
        Pitch.get_name(),
        Roll.get_name(),
        TimeWave.get_name(),
        Sin.get_name(),
        Tile.get_name()
    ]

dict_filter = {
    Y.get_name(): Y,
    X.get_name(): X,
    T.get_name(): T,
    Yaw.get_name(): Yaw,
    Pitch.get_name(): Pitch,
    Roll.get_name(): Roll,
    TimeWave.get_name(): TimeWave,
    Sin.get_name(): Sin,
    Tile.get_name(): Tile
}

def get_filter_by_name(name: str):
    if name in dict_filter:
        return dict_filter[name]
    else:
        raise Exception(f"Filter {name} not found")