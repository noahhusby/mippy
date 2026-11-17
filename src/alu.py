
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: alu.py
Description: 32-bit ALU constructed from 1-bit ALU cells.
"""
from enum import Enum

from const import MASK32


class ALUOperation(Enum):
    """Enum for ALU operations."""
    AND = 1
    OR = 2
    ADD = 3
    SUB = 4


class ALU:
    """32-bit ALU constructed from individual 1-bit ALU cells."""

    @staticmethod
    def alu_1bit(a: int, b: int, carry_in: int, operation: ALUOperation):
        """Execute one bit of an ALU operation."""

        if operation == ALUOperation.AND:
            return a & b, 0

        if operation == ALUOperation.OR:
            return a | b, 0

        if operation in (ALUOperation.ADD, ALUOperation.SUB):
            result = a ^ b ^ carry_in
            carry_out = (a & b) | (carry_in & (a ^ b))
            return result, carry_out

        raise ValueError(f"Unsupported ALU operation: {operation}")

    def execute(self, a: int, b: int, operation: ALUOperation) -> int:
        """Execute a 32-bit operation using 32 ALU cells."""

        a &= MASK32
        b &= MASK32

        # Subtraction uses two's complement: A + (~B) + 1
        # Invert B and initialize the carry-in to 1 for subtraction.
        if operation == ALUOperation.SUB:
            b = (~b) & MASK32
            carry = 1
        else:
            carry = 0

        result = 0

        for i in range(32):
            a_bit = (a >> i) & 1
            b_bit = (b >> i) & 1

            # The carry-out propagates to the next ALU cell.
            result_bit, carry = self.alu_1bit(
                a_bit, b_bit, carry, operation
            )

            result |= result_bit << i

        return result & MASK32
