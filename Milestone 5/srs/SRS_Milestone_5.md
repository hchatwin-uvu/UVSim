# UVSim Software Requirements Specification — Milestone 5
Team A | November 2026 | Draft pending final integration verification

## Scope
This document extends the Milestone 4 SRS. Existing requirements remain applicable except where the expanded machine format, conversion, and multi-document workflows supersede them. See `Milestone 4/srs/SRS_Final_Document.md` for FR-01–FR-36. The requirements below are the Milestone 5 target specification, not a claim that all features are already verified.

## Revised requirements
- **FR-02 (revised):** Load at most 250 nonblank six-digit program words into the editor, preserving malformed entries for correction where the supported GUI loader permits it.
- **FR-03 (revised):** READ accepts signed integer data within the new six-digit word range (-999999 to 999999), subject to backend validation.
- **FR-05 (revised):** WRITE displays six magnitude digits, retaining the sign of negative values.
- **FR-28 (revised):** Add a new zero word in six-digit format, subject to the 250-entry capacity.
- **FR-31:** Cut selected editor entries and place them on the clipboard.
- **FR-31a:** Copy selected editor entries without changing the source.
- **FR-31b:** Paste valid clipboard entries, rejecting invalid words or overflow without partial modification.
- **FR-32 (revised):** Reject any load, add, or paste that would exceed 250 words, preserving existing data.
- **FR-33 (revised):** Disable source mutation and document switching during running, waiting for READ, and stepping; restore normal interaction after completion or Stop.

## New functional requirements
- **FR-37 — Memory capacity:** The machine shall expose exactly 250 addressable registers, numbered 000 through 249.
- **FR-38 — Word encoding:** The simulator shall support signed six-digit BasicML words representing either instructions or data. Instruction words shall use a three-digit opcode followed by a three-digit operand. Existing BasicML operations shall retain their semantics using the expanded instruction format.
- **FR-39 — Address validation:** Instructions referencing memory shall reject addresses outside 000–249.
- **FR-40 — Arithmetic bounds:** Arithmetic shall use the new signed six-digit numeric limits and retain the existing overflow behavior at those limits.
- **FR-41 — Legacy recognition:** The loader shall distinguish supported four-digit and six-digit file formats and reject mixed-format files.
- **FR-42 — Legacy instruction conversion:** Recognized four-digit instructions shall convert to six-digit instructions by padding opcode and operand separately, e.g. 1007 to 010007.
- **FR-43 — Legacy data conversion:** Four-digit data shall convert to six-digit data without changing value or sign, e.g. 5555 to 005555. A legacy word whose first two digits are a valid opcode shall be interpreted as an instruction.
- **FR-44 — Non-destructive conversion:** Conversion shall not overwrite the original legacy file; the user shall select a destination and be able to cancel.
- **FR-45 — Conversion failures:** Invalid formats and failed writes shall be reported without losing editor content or the source file.
- **FR-46 — Multiple documents:** One application instance shall support multiple open files using tabs.
- **FR-47 — Independent document state:** Each tab shall retain its own source, filename, and unsaved-change state.
- **FR-48 — Selected-document execution:** Run shall execute the selected tab's current contents through one shared execution engine.
- **FR-49 — Execution interlock:** The application shall prevent tab switching while running, waiting for input, or stepping, until execution completes or stops.
- **FR-50 — Unsaved tab closing:** Closing a tab or the application shall offer appropriate save/discard/cancel handling and preserve the document if saving fails or is canceled.
- **FR-51 — Editor formatting:** Editor addresses shall display three digits and words shall display six digits, with a maximum of 250 entries.

## Quality and verification
No partial loads or saves; failures must preserve data. Test address 000 and 249, invalid address 250, 250 vs. 251 entries, numeric boundaries, overflow, conversion including signs and ambiguity rule, tab isolation, switching interlock, canceled saves, and repeated execution. Record actual test results in verification documentation.
