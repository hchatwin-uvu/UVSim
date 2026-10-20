"""
@Author Hunter Gadbois

Implements read write load and store operations.
"""
from word import Word

def handle_read(sim, operand: int, input_file_obj) -> None:
  line=input_file_obj.readline().strip()
  if not line:
    raise EOFError("Unexpected end of input file during READ operation.")
  val = int(line)
  if -9999 <= val <= 9999:
    sim.memory[operand] = Word(val)
  else:
    raise ValueError(f"Value {val} out of 4-digit signed word range.")

def format_word(value: int) -> str:
  """Four magnitude digits with a separate minus sign for negative values."""
  return ("-" if value < 0 else "") + f"{abs(value):04d}"


def handle_write (sim, operand: int) -> None:
  value = sim.memory[operand].value
  print(format_word(value))

def handle_load(sim, operand: int) -> None:
  sim.accumulator = sim.memory[operand].value

def handle_store(sim, operand: int) -> None:
  # Arithmetic truncation keeps the accumulator within the Word range
  sim.memory[operand] = Word(sim.accumulator)
