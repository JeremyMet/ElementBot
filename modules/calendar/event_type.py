from enum import Enum, auto;

class event_type(Enum):
    T = auto();
    DT = auto();
    MDT = auto();
    YMDT = auto();
    ERROR = auto();
    OK = auto();
