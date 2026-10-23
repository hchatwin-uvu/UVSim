# WP-1 feedback changes

October 16, 2026, feature/milestone-4-branding.

- Added the visible Selected File Name label (TODO-3).
- Moved status and READ input above output (TODO-2).
- Connected Run to controller.load_program using cached source words, allowing
  repeat runs after HALT, Stop, or errors without disk access (TODO-1 UI side).
- Updated README controls in on-screen order and documented reset behavior.
- Added UVU branding and startup theme.ini configuration.

Editor/FileActions integration and the team's architecture work remain separate
pending tasks. See verification.md for tested scope and remaining checks.

## October 20 integration

The editor is embedded beside output with shared READ controls above both.
Run now uses current editor contents, replacing the temporary original-source
cache. A fresh run preserves edited source and clears execution state/output.
Open/Close protect unsaved edits with a temporary discard confirmation until
save-aware FileActions is available. README and the current wireframe are updated.

## Save integration — October 23

On feature/save-gui-integration, WP-3 file actions and editor execution are
connected. Malformed words now load for correction using load_source/set_entries;
Run/Save require valid words. Oversized files are rejected without truncation.
Open/Close offer Save, Discard, Cancel, preserving edits if saving fails or is
canceled. The README and wireframe describe the integrated controls. Previous
pending-file-integration notes above are historical. Final team document audit,
manual visual review, and submission review remain.

## Documentation cleanup — October 23

Final documents now live under Milestone 4; see [README.md](README.md).
The SRS moves NFR-02 modularity into internal design guidance and reclassifies
NFR-04 recovery as FR-26. Class definitions document the completed separation
of ProgramStore from SimulatorController and Word-based memory/register
formatting. The current use cases and test register describe integrated editing,
saving, theming, and reruns. Earlier pending architecture/integration/document
notes are historical; manual acceptance and team submission review remain.
