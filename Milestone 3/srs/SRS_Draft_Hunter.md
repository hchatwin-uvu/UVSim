FR- 01. Select and load a text file — Accept a filename via the gui.


FR- 02.Validate file — ensure program files are extracted to four-digit words, skip blank lines, reject malformed words, and enforce the word maximum.


FR- 03. Initialization of machine state — ensure that memory has been reset before execution begins.


FR- 04. READ — Accept user input as a signed integer (-9999 to 9999) to store it at a specified memory address  if its within a valid range


FR- 05.  WRITE — Display the value at a specified memory address with four zero-padded digits and a separate minus sign for negative values.


FR- 06. LOAD  — Copy a value from a specified memory address into the accumulator.


FR- 07. STORE  — Copy the accumulator value into a specified memory address while replacing its previous contents.


FR- 08. ADD  — Add the value at a specified memory address to the accumulator


FR- 09. SUBTRACT — Subtract the value at a specified memory address from the accumulator


FR- 10. MULTIPLY — Multiply the accumulator by the value at a specified memory address


FR- 11. DIVIDE — Divide the accumulator by the value at a specified memory address


FR- 12. BRANCH unconditionally  — Jump execution to any specified memory address 


FR- 13. BRANCH if negative  — Jump to a specified address only if the accumulator is negative


FR- 14. BRANCH if zero — Jump to a specified address only if the accumulator equals zero


FR- 15. Execute program and HALT  — Repeatedly fetch, decode, and execute instructions sequentially until a HALT instruction is encountered


NFR-01 Usability: The simulator must present clear prompts and formatting that are understandable to the user.


NFR-02 Error handling — All file, validation, runtime, and arithmetic errors must produce clear, descriptive error messages to standard error and exit with status 1.


NFR-03 Modularity— The system must separate concerns across distinct modules
