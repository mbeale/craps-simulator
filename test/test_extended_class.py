import unittest
import numpy as np

from craps_sim.events import Events, Event
from craps_sim.simulator import CrapsSimulator
from craps_sim.hard_ways import HardWays,CreateNewHardways


class TripleParleyHardWays(HardWays):
    parley_count: int = 0
    original_bet_amount: float = 5.0

    def handle_point_made(self, event: Event):
        returned_event = super().handle_point_made(event)
        if returned_event.id == Events.COLLECT_WINNINGS:
            if self.parley_count < 3:
                self.parley_count += 1
                self.bet_amount += returned_event.data['amount']
                return Event(id=Events.PLACE_BET, data=returned_event.data)
            else:
                self.parley_count = 0
                take_down = self.bet_amount - self.original_bet_amount
                winnings = self.bet_amount + returned_event.data['amount'] - self.original_bet_amount
                self.bet_amount = self.original_bet_amount
                return [
                    Event(id=Events.COLLECT_WINNINGS, data={'amount': winnings}), 
                    Event(id=Events.BET_TAKE_DOWN, data={'amount': take_down})
                ]
        return returned_event

class TestSimulatorSummary(unittest.TestCase):

    def test_extend_hardways(self):
        t = TripleParleyHardWays()
        t.original_bet_amount = 5
        t.bet_amount = 5
        t.set_hard_way = 8
        t.play_when_point_is_hard_way = True
        simulator = CrapsSimulator()
        simulator.add_bets([t])
        simulator.generate_rolls(10000)
        results = simulator.simulate()
        print(f" money lost: {np.sum(results['shooters']['money_lost'])} money won: {np.sum(results['shooters']['money_won'])}")

         


