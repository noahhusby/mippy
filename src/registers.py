
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: registers.py
Description: 32-bit MIPS general-purpose register file.
"""
from const import MASK32


class RegisterFile:
    """32 general-purpose, 32-bit MIPS registers."""

    def __init__(self):
        self.registers = [0] * 32

    def read(self, index: int) -> int:
        """Read the unsigned 32-bit value of a register."""
        return self.registers[index]

    def write(self, index: int, value: int) -> None:
        """Write a 32-bit value, except to register $zero."""

        # We wouldn't want to override $zero!
        if index != 0:
            self.registers[index] = value & MASK32

    def __str__(self) -> str:
        """Return all non-zero registers as a formatted string."""
        return "\n".join(
            f"${index:02d}: 0x{value:08X}"
            for index, value in enumerate(self.registers)
            if value != 0
        )