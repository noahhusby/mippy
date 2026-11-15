
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: decoder.py
Description: MIPS machine instruction decoding.
"""

from dataclasses import dataclass

from const import OPCODES


@dataclass(frozen=True)
class Instruction:
    """Decoded MIPS instruction fields."""

    name: str
    format: str
    opcode: int
    rs: int
    rt: int
    rd: int
    shamt: int
    funct: int
    immediate: int


class Decoder:
    """Decode 32-bit MIPS machine instructions."""

    # R-format function codes
    FUNCTIONS = {
        0x20: "add",
    }

    @staticmethod
    def decode(instruction: int) -> Instruction:
        """Decode a 32-bit machine instruction."""

        if not 0 <= instruction <= 0xFFFFFFFF:
            raise ValueError("Instruction must be a 32-bit unsigned integer")

        # Extract instruction fields
        opcode = (instruction >> 26) & 0x3F
        rs = (instruction >> 21) & 0x1F
        rt = (instruction >> 16) & 0x1F
        rd = (instruction >> 11) & 0x1F
        shamt = (instruction >> 6) & 0x1F
        funct = instruction & 0x3F
        immediate = instruction & 0xFFFF

        if opcode == 0:
            # R-format instruction
            if funct not in Decoder.FUNCTIONS:
                raise ValueError(
                    f"Unsupported R-format function: 0x{funct:02X}"
                )

            name = Decoder.FUNCTIONS[funct]
            instruction_format = "R"

            # ADD requires shamt = 0
            if shamt != 0:
                raise ValueError("ADD instruction requires shamt = 0")

        elif opcode in OPCODES:
            # I-format instruction
            name = OPCODES[opcode]
            instruction_format = "I"

        else:
            raise ValueError(f"Unsupported opcode: 0x{opcode:02X}")

        return Instruction(
            name=name,
            format=instruction_format,
            opcode=opcode,
            rs=rs,
            rt=rt,
            rd=rd,
            shamt=shamt,
            funct=funct,
            immediate=immediate,
        )
