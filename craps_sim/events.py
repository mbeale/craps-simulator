from enum import Enum
import json
from dataclasses import dataclass, field

class Events(Enum):
    NO_OP = 0
    SEVEN_OUT = 1
    ESTABLISH_POINT = 2
    ROLL = 3
    NEW_SHOOTER = 4
    PLACE_BET = 5
    LOST_BET = 6
    POINT_MADE = 7
    BET_TAKE_DOWN = 8
    COLLECT_WINNINGS = 9

@dataclass
class Event():
    id: Events
    data: dict = field(default_factory=dict)