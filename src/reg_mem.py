
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: reg_mem.py
Description: 32-bit word-addressable memory and register file implementations.
"""

from const import MASK32


class Memory:
    """32-bit word-addressable memory."""

    def __init__(self, size: int = 1024):
        self.size = size
        self.words = [0] * size

    def read(self, address: int) -> int:
        """Read a 32-bit word from memory."""
        return self.words[address]

    def write(self, address: int, value: int) -> None:
        """Write a 32-bit word to memory."""
        self.words[address] = value & MASK32

    def load(self, data: list[int], start: int = 0) -> None:
        """Load a sequence of 32-bit words into memory."""
        for offset, value in enumerate(data):
            self.write(start + offset, value)

    def __str__(self) -> str:
        """Return all non-zero memory words as a formatted string."""
        return "\n".join(
            f"[{address:04d}]: 0x{value:08X}"
            for address, value in enumerate(self.words)
            if value != 0
        )

class RegisterFile(Memory):
    """32 general-purpose, 32-bit MIPS registers."""

    def __init(self) -> None:
        super().__init__(32)

    def write(self, address: int, value: int) -> None:
        """Write a 32-bit value, except to register $zero."""

        # We wouldn't want to override $zero!
        if address != 0:
            super().write(address, value)