# Test plan starter
The assignment requires a spreadsheet; create and commit the actual spreadsheet
before submission. This Markdown plan is not the spreadsheet deliverable.

Use columns: Test name | Short description | Use-case ID | Inputs/setup |
Expected outputs/state | Pass/fail criterion. Add actual result/status if useful.
Map each automated test to an approved use case and keep the sheet synchronized.

The proposed 14 use cases require at least 28 tests. Include normal and boundary/
failure paths rather than only the supplied programs. Cover zero and negative
arithmetic, divide-by-zero and agreed overflow policy, conditional branches
taken/not taken, HALT, input validation, file errors, memory capacity, and invalid
instructions. Expand coverage as policy decisions require.

Integration checks after implementation:
- Test1: 7 and 5 -> 12; also test negative and zero values within word limits.
- Test2: 7 and 5 -> 7; reverse ordering and check equal values.
- Add programs for DIVIDE, MULTIPLY, BRANCH, and BRANCHZERO.
- Record expected output and the chosen error behavior for each case.

Run from repository root: python -m unittest discover -s tests -v.
The starter includes no unit tests. A zero-test run is not evidence of correctness.
