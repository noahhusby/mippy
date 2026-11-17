
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: assembler.py
Description: MIPS assembly to machine code conversion.
"""

import re

from const import ASSEMBLER_OPCODES, REGISTERS


def register_number(name: str) -> int:
    """Convert a register name to its index."""
    name = name.strip().lower().removeprefix("$")

    if name in REGISTERS:
        return REGISTERS[name]

    if name.isdecimal() and 0 <= int(name) < 32:
        return int(name)

    raise ValueError(f"Unknown register: ${name}")


def encode_r(rs: int, rt: int, rd: int, funct: int) -> int:
    """Encode an R-type instruction."""
    return (rs << 21) | (rt << 16) | (rd << 11) | funct


def encode_i(opcode: int, rs: int, rt: int, imm: int) -> int:
    """Encode an I-type instruction."""
    return (
        (opcode << 26)
        | (rs << 21)
        | (rt << 16)
        | (imm & 0xFFFF)
    )


def assemble_instruction(line: str, labels: dict, pc: int) -> int:
    """Convert one assembly instruction into machine code."""
    mnemonic, *args = re.split(r"[\s,]+", line.strip())
    mnemonic = mnemonic.lower()

    if mnemonic == "add":
        rd, rs, rt = map(register_number, args)
        return encode_r(rs, rt, rd, 0x20)

    if mnemonic in ("lw", "sw"):
        rt = register_number(args[0])
        offset, rs = args[1].rstrip(")").split("(")
        return encode_i(
            ASSEMBLER_OPCODES[mnemonic],
            register_number(rs),
            rt,
            int(offset, 0),
        )

    if mnemonic in ("beq", "bne", "andi"):
        first = register_number(args[0])
        second = register_number(args[1])
        target = args[2]

        if mnemonic == "andi":
            rs, rt = second, first
            imm = int(target, 0)
        else:
            rs, rt = first, second
            imm = labels[target] - (pc + 1) if target in labels else int(target, 0)

        return encode_i(ASSEMBLER_OPCODES[mnemonic], rs, rt, imm)

    raise ValueError(f"Unsupported instruction: {mnemonic}")


def assemble(program: str) -> list[int]:
    """Assemble a program using two passes for label resolution."""
    labels = {}
    instructions = []

    for line in program.splitlines():
        line = line.split("#")[0].strip()

        while ":" in line:
            label, line = line.split(":", 1)
            label = label.strip()

            if not re.fullmatch(r"[A-Za-z_]\w*", label):
                raise ValueError(f"Invalid label: {label}")
            if label in labels:
                raise ValueError(f"Duplicate label: {label}")

            labels[label] = len(instructions)
            line = line.strip()

        if line:
            instructions.append(line)

    return [
        assemble_instruction(line, labels, pc)
        for pc, line in enumerate(instructions)
    ]
