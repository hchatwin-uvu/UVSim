# UVSim — Milestone 5

Milestone 5 is the final development milestone. This folder contains the team plan, updated specifications, use cases, architecture notes, GUI wireframe notes, verification tracker and coordination log.

## Contents
- [Milestone 5 plan](milestone-5.md)
- [Updated SRS](srs/SRS_Milestone_5.md)
- [Use cases](use-cases.md)
- [Class definitions and class diagram](class-definitions.md)
- [GUI wireframe and explanation](gui-design/README.md)
- [Task 4 verification tracker](verification-task4.md)
- [Coordination and meeting log](meetings/coordination-log.md)

## Implemented behavior
UVSim expands to 250 registers (000–249) and signed six-digit words, with three-digit opcodes and addresses. Legacy four-digit files are converted one-way into six-digit files while preserving the original. The application supports multiple open tabs with independent contents, paths and unsaved flags. One shared engine runs the active tab. Tab switching is blocked during execution or input wait. The editor rejects more than 250 entries.

**Integration status:** Tasks 1–3 are merged; 155 tests passed on November 13, 2026. Remaining visual checks and actual meeting records are tracked in the verification and coordination documents.
