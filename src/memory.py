
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
        self._validate(address)
        return self.words[address]

    def write(self, address: int, value: int) -> None:
        """Write a 32-bit word to memory."""
        self._validate(address)
        self.words[address] = value & MASK32

    def load(self, data: list[int], start: int = 0) -> None:
        """Load a sequence of 32-bit words into memory."""
        if start < 0 or start + len(data) > self.size:
            raise IndexError("Program exceeds memory bounds")

        for offset, value in enumerate(data):
            self.write(start + offset, value)

    def reset(self) -> None:
        """Clear all memory words."""
        self.words = [0] * self.size

    def dump(self, start: int = 0, count: int = 16) -> None:
        """Print a range of memory words."""
        if count < 0 or start < 0 or start + count > self.size:
            raise IndexError("Invalid memory range")

        for address in range(start, start + count):
            print(f"[{address:04d}]: 0x{self.words[address]:08X}")

    def _validate(self, address: int) -> None:
        if not 0 <= address < self.size:
            raise IndexError(f"Invalid memory address: {address}")
