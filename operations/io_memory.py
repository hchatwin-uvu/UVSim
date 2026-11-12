"""
@Author Hunter Gadbois

Implements read write load and store operations.
"""
from word import Word, MAX_WORD, MIN_WORD, WORD_DIGITS
from uvsim import check_address

def handle_read(sim, operand: int, input_file_obj) -> None:
  check_address(operand, "READ address")
  line=input_file_obj.readline().strip()
  if not line:
    raise EOFError("Unexpected end of input file during READ operation.")
  val = int(line)
  if MIN_WORD <= val <= MAX_WORD:
    sim.memory[operand] = Word(val)
  else:
    raise ValueError(f"Value {val} out of 6-digit signed word range.")

def format_word(value: int) -> str:
  """Six magnitude digits with a separate minus sign for negative values."""
  return ("-" if value < 0 else "") + f"{abs(value):0{WORD_DIGITS}d}"


def handle_write (sim, operand: int) -> None:
  check_address(operand, "WRITE address")
  value = sim.memory[operand].value
  print(format_word(value))

def handle_load(sim, operand: int) -> None:
  check_address(operand, "LOAD address")
  sim.accumulator = sim.memory[operand].value

def handle_store(sim, operand: int) -> None:
  check_address(operand, "STORE address")
  # Arithmetic truncation keeps the accumulator within the Word range
  sim.memory[operand] = Word(sim.accumulator)
