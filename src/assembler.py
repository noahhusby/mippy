
"""Assembler for the six supported MIPS instructions."""

import re

REGISTERS = {
    "zero": 0, "at": 1,
    "v0": 2, "v1": 3,
    "a0": 4, "a1": 5, "a2": 6, "a3": 7,
    "t0": 8, "t1": 9, "t2": 10, "t3": 11,
    "t4": 12, "t5": 13, "t6": 14, "t7": 15,
    "s0": 16, "s1": 17, "s2": 18, "s3": 19,
    "s4": 20, "s5": 21, "s6": 22, "s7": 23,
    "t8": 24, "t9": 25,
    "k0": 26, "k1": 27,
    "gp": 28, "sp": 29, "fp": 30, "ra": 31,
}

OPCODES = {
    "lw": 0x23,
    "sw": 0x2B,
    "beq": 0x04,
    "bne": 0x05,
    "andi": 0x0C,
}


def register_number(name: str) -> int:
    """Convert a register name into its 5-bit index."""
    name = name.strip().lower().removeprefix("$")

    if name.isdecimal():
        index = int(name)
        if 0 <= index < 32:
            return index
    elif name in REGISTERS:
        return REGISTERS[name]

    raise ValueError(f"Unknown register: ${name}")


def immediate_value(value: str) -> int:
    """Parse a signed decimal or hexadecimal integer."""
    return int(value.strip(), 0)


def encode_r(rs: int, rt: int, rd: int, funct: int) -> int:
    """Encode an R-format instruction."""
    return (
        (rs << 21)
        | (rt << 16)
        | (rd << 11)
        | funct
    )


def encode_i(opcode: int, rs: int, rt: int, immediate: int) -> int:
    """Encode an I-format instruction."""
    if not -32768 <= immediate <= 65535:
        raise ValueError("Immediate exceeds 16 bits")

    return (
        (opcode << 26)
        | (rs << 21)
        | (rt << 16)
        | (immediate & 0xFFFF)
    )


def assemble_instruction(line: str, labels=None, pc: int = 0) -> int:
    """Assemble one instruction into a 32-bit machine word."""
    labels = {} if labels is None else labels

    line = line.split("#", 1)[0].strip()
    if not line:
        raise ValueError("Cannot assemble an empty instruction")

    parts = line.split(None, 1)
    mnemonic = parts[0].lower()
    operands = (
        [p.strip() for p in parts[1].split(",")]
        if len(parts) == 2 else []
    )

    if mnemonic == "add":
        if len(operands) != 3:
            raise ValueError("ADD requires rd, rs, rt")

        rd, rs, rt = map(register_number, operands)
        return encode_r(rs, rt, rd, 0x20)

    if mnemonic in ("lw", "sw"):
        if len(operands) != 2:
            raise ValueError(f"{mnemonic} requires rt, offset(rs)")

        rt = register_number(operands[0])
        match = re.fullmatch(
            r"\s*([^()]+)\(\s*(\$[A-Za-z0-9]+)\s*\)\s*",
            operands[1],
        )
        if not match:
            raise ValueError("Expected memory operand: offset($rs)")

        offset = immediate_value(match.group(1))
        rs = register_number(match.group(2))

        if not -32768 <= offset <= 32767:
            raise ValueError("Memory offset must be signed 16-bit")

        return encode_i(OPCODES[mnemonic], rs, rt, offset)

    if mnemonic in ("beq", "bne"):
        if len(operands) != 3:
            raise ValueError(f"{mnemonic} requires rs, rt, offset")

        rs = register_number(operands[0])
        rt = register_number(operands[1])
        target = operands[2]

        if target in labels:
            offset = labels[target] - (pc + 1)
        else:
            offset = immediate_value(target)

        if not -32768 <= offset <= 32767:
            raise ValueError("Branch offset must be signed 16-bit")

        return encode_i(OPCODES[mnemonic], rs, rt, offset)

    if mnemonic == "andi":
        if len(operands) != 3:
            raise ValueError("ANDI requires rt, rs, immediate")

        rt = register_number(operands[0])
        rs = register_number(operands[1])
        immediate = immediate_value(operands[2])

        if not 0 <= immediate <= 65535:
            raise ValueError("ANDI immediate must be unsigned 16-bit")

        return encode_i(OPCODES[mnemonic], rs, rt, immediate)

    raise ValueError(f"Unsupported instruction: {mnemonic}")


def assemble(program: str) -> list[int]:
    """Assemble a program, resolving labels in two passes."""
    labels = {}
    instructions = []

    # First pass: collect label addresses
    for source_line in program.splitlines():
        line = source_line.split("#", 1)[0].strip()

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

    # Second pass: encode instructions
    return [
        assemble_instruction(line, labels, pc)
        for pc, line in enumerate(instructions)
    ]
