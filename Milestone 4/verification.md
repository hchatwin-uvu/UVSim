# WP-1 verification

October 16, 2026. Base: main 46630b5; branch: feature/milestone-4-branding.

## Executed checks

- `python -m unittest discover -s tests`: 76 tests passed, zero skips.
  Uses Python 3.13 and real Tk widgets on Windows.
- Real-window tests run Test1, Test2, Test3, Test3b, and Test4 to completion,
  assert rendered WRITE values, and repeat each run while file reading is blocked.
- Test5 is rejected by the existing loader and preserves the previous filename.
  Loading malformed text for editing awaits the editor/store implementation.
- Stop and runtime-error recovery rerun the original source with fresh READ
  values. Tests assert enabled Run controls and replacement rather than duplicated
  output, including consecutive runs producing the same number of results.
- Layout assertions verify Selected File Name and status above READ above output.
- Configuration tests cover UVU defaults, custom hex values, invalid/missing keys,
  malformed/duplicate INI, unreadable paths, and invalid UTF-8. Real widgets assert
  custom button/header/text/selection colors. Default path is independent of cwd.
- `git diff --check`: passed.

The initial sandbox test run could not write temporary configuration files;
rerunning outside the sandbox passed. GUI tests were not skipped.

## Remaining team integration checks

- Embed the implemented editor and file actions; replace the temporary cached
  source with editor contents for Run and route file actions through WP-3.
- Verify edited/malformed source correction, Save/Save As, unsaved-change prompts,
  and edit/save/reopen/run. These dependencies remain placeholders on this base.
- Reapply theme after constructing all new widgets; review final editor layout
  at minimum window size and with a custom palette.
- Perform final fresh-clone installation and all workflows using README.txt alone.
- Complete manual visual review of the final combined app and submitter review.

The annotated SVG describes the current WP-1 design; it is not a screenshot or
proof of completed editor/save integration. No fresh-clone or final visual review
is claimed by this record.

## October 20 editor integration verification

Branch: feature/editor-gui-integration, based on main 3580ca2.
`python -m unittest discover -s tests`: **92 tests passed, zero skips**.
The full suite required unsandboxed execution for temporary theme files; the
editor/GUI checks also passed within the sandbox. Test-window cleanup cancels
scheduled callbacks and bypasses discard prompts explicitly.

New real-widget checks verify:
- Unsaved editor changes affect each execution and remain unchanged/dirty after it.
- In-progress cell editing is committed before Run, without needing Enter first.
- Invalid/empty editor contents do not execute the previously loaded program.
- Editing is blocked while waiting for READ; Copy works and Stop restores editing.
- Canceling discard preserves file path, edits, and the open window; accepting
  discard replaces source and clears dirty state.
- At 1000x620, READ is above both columns, editor is left of output, and both
  content areas have usable height. Existing instructor/rerun tests still pass.

The editor embedding and edited-source execution tasks from October 16 are now
complete. FileActions/ProgramStore, Save/Save As, malformed file correction,
full edit/save/reopen acceptance, final manual visual review, and fresh-clone
verification remain pending. The updated SVG documents the integrated layout.

## October 23 save integration verification

Base main: 5cf3e2f. Branch: feature/save-gui-integration.
`python -m unittest discover -s tests`: **112 passed, zero skips**.

Real Tk integration tests exercise malformed open, rejected Run, correction,
execution, Save As to a temporary directory, filename/dirty-state updates, further
editing, Save, reopen, and repeated execution. The original malformed file is
preserved by Save As. Tests also cover canceled Save As during an Open prompt,
failed saves preventing discard, successful save-before-open, and oversized-file
rejection preserving existing editor contents. Existing atomic-write tests verify
that replacement failure preserves the original file and cleans temporary files.
All instructor program, controller, editor, GUI, and theme tests pass.

Files over 100 nonblank entries remain rejected without truncation. Malformed
BasicML words within that limit load and highlight for repair. UTF-8 decoding
errors remain file-read errors. Save requires valid words; invalid drafts are
not written. Validation line numbers refer to editor rows, not skipped blank
file lines. Save/Discard/Cancel is shared by Open and Close.

The prior pending save/malformed-word integration notes are resolved. Manual
visual review of the final combined app, fresh-clone verification, final team
document audit, and submission approval are not claimed by these test results.

## October 23 final documentation audit

Branch renamed to `feature/save-gui-integration-docs`; implementation changes
remain on this branch. Current deliverables are indexed in [README.md](README.md).
Earlier milestone documents and dated verification notes remain historical.

- Audited the final SRS against implemented editor, save, rerun, configuration,
  validation, capacity, and recovery behavior. Retained FR-01–25 identifiers;
  added FR-26–42. Former NFR-02 is now an internal architecture principle;
  former NFR-04 recovery is functional FR-26.
- Updated use cases UC-01–21 and added UC-22–26 for Save, Save As, themes,
  unsaved-change decisions, and Stop. Distinguished strict console loading
  from editable GUI source loading.
- Matched all 10 runtime classes and 77 declared methods/properties against
  the Python AST; documented Word memory, integer accumulator, file access,
  source/dirty-state ownership, and execution state. Added a class diagram.
- Matched all 112 workbook rows to exact executable test methods and the
  successful October 23 run (Python 3.13, Windows, real Tk, zero skips).
  Preserved UT-01–36, corrected Word expectations, validated use-case IDs,
  and checked table coverage, populated cells, and formula-error scan.
- Exported SRS, use cases, and class definitions PDFs; rendered and inspected
  all 25 pages. Inspected workbook renders at the start, middle, and end.
  Updated repository/test README links to the current deliverables.

The document-audit item is complete. The remaining acceptance work is final
manual app/readability review, a dedicated NFR-05 two-second startup measurement,
fresh-clone verification, and team submission/meeting-report review. Automated
suite duration is not a measurement of NFR-05. No new runtime behavior was
changed as part of this documentation audit.
