# WP-1 user-guide contribution

These instructions describe the WP-1 window once WP-2/WP-3 are integrated. For now, `python main.py --gui` displays an integration-pending notice; `python main.py` remains the working console launcher.

- **Open file:** Choose a BasicML file anywhere you can access it. The repository includes samples under `programs/`, including runnable Test1.txt and Test2.txt. Files do not have to be in that folder. Cancel leaves the current session unchanged.
- **Selected filename:** The last successfully loaded path. A failed load leaves the previous name visible and explains the failure in the status area.
- **Run:** Start a loaded program. Available only when loading succeeded and the controller is ready.
- **Stop:** Stop a running program or pending input request. Open a file again for a new run. Stop first if you want to change files during execution.
- **Status/error area:** Read messages here for input requests, errors, completion, or stopping. For file errors, choose Open file again. For READ errors, correct the input and resubmit without starting the program over.
- **Close:** Close the application using the normal window close control.

Python 3.10+ with Tcl/Tk support is required. Check with `python -m tkinter`. No third-party pip packages are needed. WP-3 supplies the final READ/Submit/output instructions; WP-4 assembles and verifies the complete README and platform-specific installation directions.
