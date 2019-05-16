import unittest
import numpy as np
from craps_sim.events import Events
from craps_sim.hard_ways import CreateNewHardways
from craps_sim.simulator import CrapsSimulator

class TestHardWays(unittest.TestCase):

    @unittest.expectedFailure
    def test_set_hard_way(self):
        self.assertEqual(0, CreateNewHardways(7,5.0))

    def test_handle_seven_out(self):
        hw = CreateNewHardways(8, 5.0)
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[4,6],[3,4],[3,3],[3,4]]))
        simulator.add_bets(hw)
        simulator.simulate()
        self.assertEqual(2, len([x for x in simulator.events if x.id == Events.LOST_BET]))

    def test_handle_seven_always_working(self):
        hw = CreateNewHardways(8, 5.0, always_work=True)
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[4,6],[5,5],[4,4],[4,4]]))
        simulator.add_bets(hw)
        simulator.simulate()
        self.assertEqual(2, len([x for x in simulator.events if x.id == Events.COLLECT_WINNINGS]))

    def test_play_when_point_is_hard_way(self):
        hw = CreateNewHardways(8, 5.0, play_when_point_is_hard_way=True)
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[4,4],[4,4],[4,4],[5,3]]))
        simulator.add_bets(hw)
        simulator.simulate()
        self.assertEqual(1, len([x for x in simulator.events if x.id == Events.COLLECT_WINNINGS]))
        self.assertEqual(1, len([x for x in simulator.events if x.id == Events.LOST_BET]))

    def test_point_made_lost_bet(self):
        hw = CreateNewHardways(8, 5.0, play_when_point_is_hard_way=True)
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[4,4],[5,3]]))
        simulator.add_bets(hw)
        simulator.simulate()
        self.assertEqual(1, len([x for x in simulator.events if x.id == Events.LOST_BET]))
        self.assertEqual(0, len([x for x in simulator.events if x.id == Events.COLLECT_WINNINGS]))
 
    def test_handle_roll_win(self):
        hw = CreateNewHardways(8, 5.0)
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[3,3],[4,4]]))
        simulator.add_bets(hw)
        simulator.simulate()
        self.assertEqual(0, len([x for x in simulator.events if x.id == Events.LOST_BET]))
        self.assertEqual(1, len([x for x in simulator.events if x.id == Events.COLLECT_WINNINGS]))
         
     
    def test_handle_roll_lost(self):
        hw = CreateNewHardways(8, 5.0)
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[3,3],[5,3]]))
        simulator.add_bets(hw)
        simulator.simulate()
        self.assertEqual(1, len([x for x in simulator.events if x.id == Events.LOST_BET]))
        self.assertEqual(0, len([x for x in simulator.events if x.id == Events.COLLECT_WINNINGS]))
         
    def test_multiple_wins_and_losses(self):
        hw = CreateNewHardways(8, 5.0)
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[3,3],[5,3],[2,4],[2,3],[4,3],[4,2],[4,4],[3,3],[2,3],[4,4]]))
        simulator.add_bets(hw)
        simulator.simulate()
        self.assertEqual(2, len([x for x in simulator.events if x.id == Events.LOST_BET]))
        self.assertEqual(2, len([x for x in simulator.events if x.id == Events.COLLECT_WINNINGS]))
       
 


