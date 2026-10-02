"""Launch the GUI by default; retain an explicit console compatibility mode."""
import argparse
import sys

from loader import load_program
from uvsim import UVSim


def main() -> int:
    parser = argparse.ArgumentParser(description="UVSim BasicML simulator")
    parser.add_argument("file", nargs="?", help="BasicML program file")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--gui", action="store_true", help="Launch the GUI (default)")
    mode.add_argument("--console", action="store_true", help="Run the legacy console interface")
    args = parser.parse_args()
    if not args.console:
        from gui.app import launch
        launch(args.file)
        return 0
    try:
        path = args.file or input("BasicML program file: ").strip()
        if not path:
            raise ValueError("A program filename is required.")
        machine = UVSim()
        machine.load(load_program(path))
        machine.run()
    except (OSError, ValueError, NotImplementedError, EOFError) as error:
        print(f"UVSim: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
