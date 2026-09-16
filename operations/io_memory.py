"""
@Author Hunter Gadbois

Implements read write load and store operations.
"""

def handle_read(sim, operand: int, , input_file_obj) -> None:
  line=input_file_obj.readline().strip()
  if not line:
    raise EOFError("Unexpected end of input file during READ operation.")
  val = int(line)
  if -9999 <= val <= 9999:
    sim.memory[operand] = val
  else:
    raise ValueError(f"Value {val} out of 4-digit signed word range.")

def handle_write (sim, operand: int) -> None:
  value = sim.memory[operand]
  print(f"{value:05d}")

def handle_load(sim. operand: int) -> None:
  sim.accumulator = sim.memory[operand]

def handle_store(sim. operand: int) -> None:
  sim.memory[operand] = sim.accumulator
