"""One-way conversion of legacy four-digit BasicML programs."""

import os
from collections.abc import Iterable
from enum import Enum
from pathlib import Path

from program_store import ProgramStore
from uvsim import MEMORY_SIZE
from word import Word

MAX_PROGRAM_WORDS = MEMORY_SIZE
LEGACY_OPCODES = frozenset((10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43))


class ProgramFormat(str, Enum):
    """Supported signed word formats."""

    FOUR_DIGIT = "four-digit"
    SIX_DIGIT = "six-digit"


def _parse_program(
    entries: Iterable[str],
) -> tuple[ProgramFormat, list[int]]:
    program_format = None
    values = []

    for line_number, entry in enumerate(entries, start=1):
        text = entry.strip()
        if not text:
            continue
        if (len(text) not in (5, 7) or text[0] not in "+-"
                or not text[1:].isascii() or not text[1:].isdecimal()):
            raise ValueError(
                f"Invalid BasicML word on line {line_number}: expected a sign "
                "followed by four or six digits."
            )

        current_format = (
            ProgramFormat.FOUR_DIGIT if len(text) == 5
            else ProgramFormat.SIX_DIGIT
        )
        if program_format is not None and current_format != program_format:
            raise ValueError(
                f"Mixed four- and six-digit BasicML words on line {line_number}."
            )
        program_format = current_format

        value = int(text)
        limit = 9999 if current_format == ProgramFormat.FOUR_DIGIT else 999999
        if not -limit <= value <= limit:
            raise ValueError(
                f"BasicML word out of range on line {line_number}: {text}"
            )
        values.append(value)
        if len(values) > MAX_PROGRAM_WORDS:
            raise ValueError(
                f"Program contains more than {MAX_PROGRAM_WORDS} words."
            )

    if program_format is None:
        raise ValueError("Program is empty; cannot determine its word format.")
    return program_format, values


def detect_program_format(entries: Iterable[str]) -> ProgramFormat:
    """Validate entries and return their uniform four- or six-digit format."""

    program_format, _ = _parse_program(entries)
    return program_format


def convert_program(entries: Iterable[str]) -> list[Word]:

    program_format, values = _parse_program(entries)
    if program_format != ProgramFormat.FOUR_DIGIT:
        raise ValueError("Only four-digit BasicML programs can be converted.")

    converted = []
    for value in values:
        magnitude = abs(value)
        opcode, operand = divmod(magnitude, 100)
        if opcode in LEGACY_OPCODES:
            magnitude = opcode * 1000 + operand
        converted.append(Word(-magnitude if value < 0 else magnitude))
    return converted


def write_converted_program(
    destination_path: str | os.PathLike[str],
    words: Iterable[Word],
) -> None:
    """Atomically write converted six-digit words to the destination."""

    ProgramStore().save(os.fspath(destination_path), list(words))


def convert_file(
    source_path: str | os.PathLike[str],
    destination_path: str | os.PathLike[str],
) -> list[Word]:

    source = Path(source_path).resolve()
    destination = Path(destination_path).resolve()
    if source == destination:
        raise ValueError("Converted output must not overwrite the source file.")

    with source.open("r", encoding="utf-8-sig") as file:
        words = convert_program(file)
    write_converted_program(destination, words)
    return words
