
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: memory.py
Description: 32-bit word-addressable memory implementation.
"""
from const import MASK32


class Memory:
    """32-bit word-addressable memory."""

    def __init__(self, size: int = 1024):
        if size <= 0:
            raise ValueError("Memory size must be positive")

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