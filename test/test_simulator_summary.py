import unittest
import numpy as np
from craps_sim.events import Events, Event
from craps_sim.simulator import CrapsSimulator
from craps_sim.hard_ways import CreateNewHardways


class TestSimulatorSummary(unittest.TestCase):

    def test_roll_count(self):
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[4,4],[3,2],[3,3],[6,3],[5,2]]))
        results = simulator.simulate()
        self.assertEqual(5, results['shooters'][0]['roll_count'])

    def test_max_on_the_table(self):
        simulator = CrapsSimulator()
        hw = CreateNewHardways(8, 5.0, play_when_point_is_hard_way=True)
        hw2 = CreateNewHardways(8, 5.0, always_work=True)
        hw3 = CreateNewHardways(8, 5.0)
        hw4 = CreateNewHardways(8, 5.0)
        simulator.add_bets([hw,hw2,hw3,hw4])
        simulator.set_sample_data(np.array([[4,4],[3,5],[3,3],[6,3],[5,2]]))
        results = simulator.simulate()
        self.assertEqual(20.00, results['shooters'][0]['max_on_table'])

    def test_money_lost_money_won(self):
        simulator = CrapsSimulator()
        hw = CreateNewHardways(8, 5.0, play_when_point_is_hard_way=True)
        hw2 = CreateNewHardways(8, 5.0, always_work=True)
        hw3 = CreateNewHardways(8, 5.0)
        hw4 = CreateNewHardways(8, 5.0)
        simulator.add_bets([hw,hw2,hw3,hw4])
        simulator.set_sample_data(np.array([[4,4],[3,5],[3,3],[3,3],[4,4], [4,4],[3,6],[5,2]]))
        results = simulator.simulate()
        self.assertEqual(25.00, results['shooters'][0]['money_lost'])
        self.assertEqual(5, results['shooters'][0]['lost_count'])
        self.assertEqual(5*40, results['shooters'][0]['money_won'])
        self.assertEqual(5, results['shooters'][0]['win_count'])

    def test_points_established_and_won(self):
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[4,4],[3,2],[3,3],[6,3],[3,5],[5,2],[4,5],[3,6],[4,4],[5,2]]))
        results = simulator.simulate()
        self.assertEqual(3, results['shooters'][0]['points_established'])
        self.assertEqual(2, results['shooters'][0]['points_won'])


    def test_10000_simulations(self):
        simulator = CrapsSimulator()
        hw = CreateNewHardways(8, 5.0, play_when_point_is_hard_way=True)
        simulator.add_bets([hw])
        simulator.generate_rolls(10000)
        results = simulator.simulate()
        print(f"max money lost: {np.max(results['shooters']['money_lost'])} max money won: {np.max(results['shooters']['money_won'])}")

    