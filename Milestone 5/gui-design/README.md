# Milestone 5 GUI wireframe and interaction notes
Team A | Proposed interface, subject to Hayden's final implementation

```text
+--------------------------------------------------------------------------+
| UVSim | BasicML simulator                                                |
| [Open] [Save] [Save As] [Convert legacy] [Run] [Stop]                    |
| [program-a.txt *] [program-b.txt] [+]                                    |
| Selected file: program-a.txt                                             |
| Status / validation / execution messages                                 |
| +-----------------------------+ +--------------------------------------+ |
| | Program editor              | | READ input / Submit                  | |
| | [Add] [Delete] [Cut] ...    | | Output (scrollable)                  | |
| | Address | Instruction/data  | |                                      | |
| | 000     | +010007           | |                                      | |
| | ...     | ...               | |                                      | |
| | 249     | ...               | |                                      | |
| +-----------------------------+ +--------------------------------------+ |
+--------------------------------------------------------------------------+
```

This is a design wireframe, not a screenshot of a verified final build. Tabs represent independent open documents, with an asterisk indicating unsaved changes. The conversion control uses the backend's legacy conversion interface and a destination dialog. Only the active document is executed through the shared engine. Switching tabs is disabled during running, waiting for READ, or stepping. The editor shows addresses 000–249 and six-digit words, and rejects capacity overflow. Status information must be visible without resizing the initial window. Register edit text must be readable while editing and after commit. Colors are standard RGB hexadecimal values (#RRGGBB), default green #4C721D and white #FFFFFF.

Final review: compare labels, tab placement, conversion action, disabled-state behavior, and screenshot to Hayden's integrated implementation before submission.
