# UVSim — Milestone 5

Milestone 5 is the final development milestone. This folder contains the team plan, updated target specifications, use cases, architecture notes, GUI wireframe notes, verification tracker and coordination log.

## Contents
- [Milestone 5 plan](milestone-5.md)
- [Updated SRS](srs/SRS_Milestone_5.md)
- [Use cases](use-cases.md)
- [Class definitions and class diagram](class-definitions.md)
- [GUI wireframe and explanation](gui-design/README.md)
- [Task 4 verification tracker](verification-task4.md)
- [Coordination and meeting log](meetings/coordination-log.md)

## Target behavior
UVSim expands to 250 registers (000–249) and signed six-digit words, with three-digit opcodes and addresses. Legacy four-digit files are converted one-way into six-digit files while preserving the original. The application supports multiple open tabs with independent contents, paths and unsaved flags. One shared engine runs the active tab. Tab switching is blocked during execution, input wait, and stepping. The editor rejects more than 250 entries.

**Integration status:** This documentation describes planned Milestone 5 acceptance behavior. Verify and update it against the actual merged implementation before submission. Test results must be recorded rather than assumed.
