"""
Unit Tests for Mealy <-> Moore Conversion Simulator
"""

import unittest
from simulator import (
    MealyMachine, MooreMachine,
    mealy_to_moore, moore_to_mealy,
    get_preset_mealy_1s_complement,
    get_preset_mealy_sequence_detector,
    get_preset_moore_sequence_detector
)


class TestMealyMooreSimulator(unittest.TestCase):

    def test_mealy_to_moore_1s_complement(self):
        mealy = get_preset_mealy_1s_complement()
        moore, _ = mealy_to_moore(mealy)

        test_inputs = ["0", "1", "0101", "111000", ""]
        for w in test_inputs:
            _, m_out, _ = mealy.simulate(w)
            _, mo_out, _ = moore.simulate(w)
            # Moore output starts with initial state output, followed by Mealy output
            self.assertEqual(mo_out[1:], m_out)
            self.assertEqual(len(mo_out), len(m_out) + 1)

    def test_mealy_to_moore_sequence_detector(self):
        mealy = get_preset_mealy_sequence_detector()
        moore, _ = mealy_to_moore(mealy)

        test_inputs = ["0", "01", "001", "0101", "1111", "010101"]
        for w in test_inputs:
            _, m_out, _ = mealy.simulate(w)
            _, mo_out, _ = moore.simulate(w)
            self.assertEqual(mo_out[1:], m_out)
            self.assertEqual(len(mo_out), len(w) + 1)
            self.assertEqual(len(m_out), len(w))

    def test_moore_to_mealy_substring_detector(self):
        moore = get_preset_moore_sequence_detector()
        mealy, _ = moore_to_mealy(moore)

        test_inputs = ["0", "1", "10", "101", "1010", "0010100"]
        for w in test_inputs:
            _, m_out, _ = mealy.simulate(w)
            _, mo_out, _ = moore.simulate(w)
            self.assertEqual(mo_out[1:], m_out)
            self.assertEqual(len(mo_out), len(w) + 1)
            self.assertEqual(len(m_out), len(w))

    def test_state_count_split(self):
        # Mealy with state having 2 different incoming outputs must split in Moore
        mealy = get_preset_mealy_sequence_detector()
        moore, _ = mealy_to_moore(mealy)
        # q0 has incoming outputs '0' and '1', q1 has '0' -> total 3 Moore states
        self.assertEqual(len(moore.states), 3)
        self.assertIn("q0_0", moore.states)
        self.assertIn("q0_1", moore.states)
        self.assertIn("q1_0", moore.states)


if __name__ == "__main__":
    unittest.main()
