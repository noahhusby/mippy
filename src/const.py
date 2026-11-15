
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: const.py
Description: List of constants used throughout the project.
"""

MASK32 = 0xFFFFFFFF

# Supported instruction opcodes
OPCODES = {
    0x23: "lw",
    0x2B: "sw",
    0x04: "beq",
    0x05: "bne",
    0x0C: "andi",
}
