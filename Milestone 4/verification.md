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
