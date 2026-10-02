"""Focused regressions for the controller bugs found during GUI integration."""
from pathlib import Path
import unittest
from controller import SimulatorController

ROOT = Path(__file__).resolve().parents[1]

class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.c = SimulatorController()

    def load(self, name):
        return self.c.load_file(str(ROOT / 'programs' / name))

    def test_read_retry_and_single_consumption(self):
        self.assertEqual(self.c.state, 'empty')
        self.assertTrue(self.load('Test1.txt'))
        self.c.start()
        for value in ['7', '5']:
            self.c.tick()
            self.assertEqual(self.c.state, 'waiting_input')
            before = self.c.machine.memory.copy()
            counter = self.c.machine.instruction_counter
            for invalid in ['', 'abc', '1.5', '10000', '-10000']:
                self.assertFalse(self.c.submit_input(invalid))
                self.assertEqual(self.c.machine.memory, before)
                self.assertEqual(self.c.machine.instruction_counter, counter)
            self.assertTrue(self.c.submit_input(value))
            self.assertFalse(self.c.submit_input(value))
        self.c.tick()
        self.assertEqual((self.c.state, self.c.outputs), ('halted', [12]))

    def test_write_advances_and_failed_load_preserves_output(self):
        self.assertTrue(self.load('Test4.txt'))
        self.c.start(); self.c.tick()
        expected = [1111, 2222, 3333, 4444, 5555]
        self.assertEqual((self.c.state, self.c.outputs), ('halted', expected))
        self.assertFalse(self.load('Test5.txt'))
        self.assertEqual((self.c.state, self.c.outputs), ('halted', expected))
        self.assertTrue(self.load('Test1.txt'))
        self.assertEqual(self.c.outputs, [])

    def test_stop_discards_pending_read(self):
        self.load('Test1.txt'); self.c.start(); self.c.tick(); self.c.stop()
        self.assertEqual(self.c.state, 'stopped')
        self.assertIsNone(self.c._pending_read)
        self.assertFalse(self.c.submit_input('7'))

    def test_loop_is_bounded_and_can_stop(self):
        self.load('Test1.txt')
        self.c.machine.load([4000])
        self.c.start(); self.c.tick(3)
        self.assertEqual(self.c.state, 'running')
        self.c.stop()
        self.assertEqual(self.c.state, 'stopped')
