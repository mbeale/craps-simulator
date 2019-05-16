from dataclasses import dataclass
from .events import Event, Events
from .subscriber import Subscriber
import numpy as np

summary_dtype = np.dtype([
    ('max_on_table', 'f8'), 
    ('money_lost', 'f8'), 
    ('money_won', 'f8'), 
    ('lost_count', 'i4'), 
    ('win_count', 'i4'), 
    ('roll_count', 'i4'), 
    ('points_established', 'i4'), 
    ('points_won', 'i4')
    ])

class SimulatorSummary(Subscriber):

    np_array = None
    on_table: float = 0.0

    def __init__(self):
        self.np_array = np.zeros(1, dtype=summary_dtype)

    def handle_roll(self, event) -> Event:
        self.np_array['roll_count'] += 1
        return self.no_op()

    def handle_establish_point(self, event) -> Event:
        self.np_array['roll_count'] += 1
        self.np_array['points_established'] += 1
        return self.no_op()

    def handle_seven_out(self, event) -> Event:
        self.np_array['roll_count'] += 1
        return self.no_op()

    def handle_new_shooter(self, event) -> Event:
        return self.no_op()

    def handle_place_bet(self, event) -> Event:
        self.on_table += event.data['amount']
        self.np_array['max_on_table'] = self.on_table if self.on_table > self.np_array['max_on_table'] else self.np_array['max_on_table']
        return self.no_op()
 
    def handle_lost_bet(self, event) -> Event:
        self.np_array['lost_count'] += 1
        self.np_array['money_lost'] += event.data['amount']
        self.on_table -= event.data['amount']
        return self.no_op()

    def handle_collect_winnings(self, event: Event) -> Event:
        self.np_array['win_count'] += 1
        self.np_array['money_won'] += event.data['amount']
        return self.no_op()

    def handle_point_made(self, event) -> Event:
        self.np_array['roll_count'] += 1
        self.np_array['points_won'] += 1
        return self.no_op()
    