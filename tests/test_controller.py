"""Focused regressions for the controller bugs found during GUI integration."""
from pathlib import Path
import unittest
from controller import SimulatorController
from word import Word

ROOT = Path(__file__).resolve().parents[1]

WRITE_PROGRAM = [Word(v) for v in (1103, 4300, 0, 1234)]  # WRITE 03, HALT
READ_PROGRAM = [Word(v) for v in (1002, 4300)]            # READ 02, HALT
LOOP_PROGRAM = [Word(4000)]                               # BRANCH 00

class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.c = SimulatorController()

    def load(self, name):
        return self.c.load_file(str(ROOT / 'programs' / name))

    def run_to_end(self):
        self.c.start(); self.c.tick()

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
        self.c.machine.load(LOOP_PROGRAM)
        self.c.start(); self.c.tick(3)
        self.assertEqual(self.c.state, 'running')
        self.c.stop()
        self.assertEqual(self.c.state, 'stopped')

    def test_load_from_empty_enters_ready(self):
        self.assertTrue(self.c.load_program(WRITE_PROGRAM))
        self.assertEqual(self.c.state, 'ready')
        self.assertEqual(self.c.machine.memory[:4], WRITE_PROGRAM)
        self.assertEqual(self.c.outputs, [])

    def test_loaded_program_runs(self):
        self.c.load_program(WRITE_PROGRAM)
        self.run_to_end()
        self.assertEqual((self.c.state, self.c.outputs), ('halted', [1234]))

    def test_reload_from_each_inactive_state_gives_identical_run(self):
        self.c.load_program(WRITE_PROGRAM)                      # ready
        self.assertTrue(self.c.load_program(WRITE_PROGRAM))
        self.run_to_end()                                       # halted
        self.assertTrue(self.c.load_program(WRITE_PROGRAM))
        self.assertEqual((self.c.state, self.c.outputs), ('ready', []))
        self.run_to_end()
        self.assertEqual((self.c.state, self.c.outputs), ('halted', [1234]))

        self.c.load_program(LOOP_PROGRAM)
        self.c.start(); self.c.tick(3); self.c.stop()           # stopped
        self.assertEqual(self.c.state, 'stopped')
        self.assertTrue(self.c.load_program(WRITE_PROGRAM))
        self.run_to_end()
        self.assertEqual((self.c.state, self.c.outputs), ('halted', [1234]))

        self.c.load_program([Word(9900)])                       # invalid opcode
        self.run_to_end()
        self.assertEqual(self.c.state, 'error')
        self.assertTrue(self.c.load_program(WRITE_PROGRAM))
        self.run_to_end()
        self.assertEqual((self.c.state, self.c.outputs), ('halted', [1234]))

    def test_rejected_while_running_or_waiting(self):
        self.c.load_program(LOOP_PROGRAM)
        self.c.start(); self.c.tick(3)
        self.assertFalse(self.c.load_program(WRITE_PROGRAM))
        self.assertEqual(self.c.state, 'running')
        self.assertEqual(self.c.machine.memory[0], Word(4000))
        self.c.stop()

        self.c.load_program(READ_PROGRAM)
        self.c.start(); self.c.tick()
        self.assertFalse(self.c.load_program(WRITE_PROGRAM))
        self.assertEqual(self.c.state, 'waiting_input')
        self.assertTrue(self.c.submit_input('7'))

    def test_empty_and_oversized_programs_preserve_session(self):
        self.c.load_program(WRITE_PROGRAM)
        self.run_to_end()
        before = self.c.machine.memory.copy()
        for bad in ([], [Word(0)] * 101):
            self.assertFalse(self.c.load_program(bad))
            self.assertEqual((self.c.state, self.c.outputs), ('halted', [1234]))
            self.assertEqual(self.c.machine.memory, before)
            self.assertNotEqual(self.c.message, 'Program loaded successfully.')

    def test_exactly_100_words_is_accepted(self):
        self.assertTrue(self.c.load_program([Word(0)] * 100))

    def test_non_word_entries_are_a_type_error(self):
        with self.assertRaises(TypeError):
            self.c.load_program([1103, 4300])
        self.assertEqual(self.c.state, 'empty')
