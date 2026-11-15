
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: alu.py
Description: 32-bit ALU constructed from 1-bit ALU cells.
"""
from const import MASK32


class ALU:
    """32-bit ALU constructed from individual 1-bit ALU cells."""

    @staticmethod
    def alu_1bit(a: int, b: int, carry_in: int, operation: str):
        """Execute one bit of an ALU operation."""

        if operation == "AND":
            return a & b, 0

        if operation == "OR":
            return a | b, 0

        if operation in ("ADD", "SUB"):
            result = a ^ b ^ carry_in
            carry_out = (a & b) | (carry_in & (a ^ b))
            return result, carry_out

        raise ValueError(f"Unsupported ALU operation: {operation}")

    def execute(self, a: int, b: int, operation: str) -> int:
        """Execute a 32-bit operation using 32 ALU cells."""

        a &= MASK32
        b &= MASK32

        # Subtraction uses two's complement: A + (~B) + 1
        if operation == "SUB":
            b = (~b) & MASK32
            carry = 1
        else:
            carry = 0

        result = 0

        for i in range(32):
            a_bit = (a >> i) & 1
            b_bit = (b >> i) & 1

            result_bit, carry = self.alu_1bit(
                a_bit, b_bit, carry, operation
            )

            result |= result_bit << i

        return result & MASK32
