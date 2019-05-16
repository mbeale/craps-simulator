from .events import Events, Event
import json
from dataclasses import dataclass
from .odds import OddsType
from .subscriber import Subscriber

@dataclass
class Bet(Subscriber):
    working: bool = False
    bet_placed: bool = False
    bet_amount: float = 0.0
    simulation_count: int = 0
    roll_count: int = 0
    odds_type: OddsType = OddsType.ONE_TIME


 