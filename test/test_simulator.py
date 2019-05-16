import unittest
import numpy as np
from craps_sim.events import Events
from craps_sim.simulator import CrapsSimulator

class TestSimulator(unittest.TestCase):

    def test_event_flow(self):
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[4,4],[3,3],[3,3],[3,3]]))
        simulator.simulate()
        self.assertEqual([Events.NEW_SHOOTER, Events.ESTABLISH_POINT, Events.ROLL, Events.ROLL, Events.ROLL], [x.id for x in simulator.events])

    def test_establishing_point(self):
        simulator = CrapsSimulator()
        self.assertFalse(simulator.establishing_point(np.array([3, 4])))
        self.assertTrue(simulator.establishing_point(np.array([4,4])))

    def test_flip_established_point(self):
        simulator = CrapsSimulator()
        previous_value = simulator.is_point_established
        simulator.flip_established_point()
        self.assertNotEquals(previous_value, simulator.is_point_established)

    def test_seven_out(self):
        simulator = CrapsSimulator()
        simulator.set_sample_data(np.array([[1,2], [4,4],[3,4],[2,3],[3,4]]))
        simulator.simulate()
        self.assertEqual(2, len([x.id for x in simulator.events if x.id == Events.SEVEN_OUT]))

    def test_combination_builder(self):
        simulator = CrapsSimulator()
        self.assertEqual([[1, 6], [2, 5], [3, 4], [4, 3], [5, 2], [6, 1]], simulator.combinations(7))



if __name__ == '__main__':
    unittest.main()