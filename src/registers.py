
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: registers.py
Description: 32-bit MIPS general-purpose register file.
"""
from const import MASK32


class RegisterFile:
    """32 general-purpose, 32-bit MIPS registers."""

    NUM_REGISTERS = 32

    def __init__(self):
        self.registers = [0] * self.NUM_REGISTERS

    def read(self, index: int) -> int:
        """Read the unsigned 32-bit value of a register."""
        self._validate(index)
        return self.registers[index]

    def write(self, index: int, value: int) -> None:
        """Write a 32-bit value, except to register $zero."""
        self._validate(index)

        if index != 0:
            self.registers[index] = value & MASK32

    def reset(self) -> None:
        """Reset all registers to zero."""
        self.registers = [0] * self.NUM_REGISTERS

    def dump(self) -> None:
        """Print all register values in hexadecimal."""
        for index, value in enumerate(self.registers):
            print(f"${index:02d}: 0x{value:08X}")

    @staticmethod
    def _validate(index: int) -> None:
        if not 0 <= index < 32:
            raise IndexError(f"Invalid register index: {index}")
