"""Command-line entry point; simulator implementation is a team task."""
import argparse
import sys

from loader import load_program
from uvsim import UVSim


def main() -> int:
    parser = argparse.ArgumentParser(description="UVSim BasicML simulator")
    parser.add_argument("file", nargs="?", help="BasicML program file")
    parser.add_argument("--gui", action="store_true", help="Launch the GUI (requires WP-2 and WP-3)")
    args = parser.parse_args()
    if args.gui:
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
