
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: cpu.py
Description: CPU datapath and instruction execution.
"""

from alu import ALU, ALUOperation
from registers import RegisterFile
from memory import Memory
from decoder import Decoder

class CPU:
    """Single-cycle 32-bit MIPS CPU simulator."""

    def __init__(self, memory_size: int = 1024):
        self.registers = RegisterFile()
        self.data_memory = Memory(memory_size)
        self.instruction_memory = Memory(memory_size)
        self.pc = 0
        self.alu = ALU()

    def read_register(self, index: int) -> int:
        return self.registers.read(index)

    def write_register(self, index: int, value: int) -> None:
        self.registers.write(index, value)

    def read_memory(self, address: int) -> int:
        return self.data_memory.read(address)

    def write_memory(self, address: int, value: int) -> None:
        self.data_memory.write(address, value)

    @staticmethod
    def sign_extend(value: int) -> int:
        """Sign-extend a 16-bit immediate."""
        value &= 0xFFFF
        return value - 0x10000 if value & 0x8000 else value

    def execute(self, instruction: int) -> None:
        """Execute one 32-bit MIPS instruction."""

        decoded = Decoder.decode(instruction)

        rs = decoded.rs
        rt = decoded.rt
        rd = decoded.rd
        immediate = decoded.immediate

        # Default to the next instruction
        next_pc = self.pc + 1

        if decoded.name == "add":
            result = self.alu.execute(
                self.read_register(rs),
                self.read_register(rt),
                ALUOperation.ADD,
            )
            self.write_register(rd, result)

        elif decoded.name == "lw":
            address = self.alu.execute(
                self.read_register(rs),
                self.sign_extend(immediate),
                ALUOperation.ADD,
            )
            self.write_register(rt, self.read_memory(address))

        elif decoded.name == "sw":
            address = self.alu.execute(
                self.read_register(rs),
                self.sign_extend(immediate),
                ALUOperation.ADD,
            )
            self.write_memory(address, self.read_register(rt))

        elif decoded.name == "beq":
            difference = self.alu.execute(
                self.read_register(rs),
                self.read_register(rt),
                ALUOperation.SUB,
            )
            if difference == 0:
                next_pc += self.sign_extend(immediate)

        elif decoded.name == "bne":
            difference = self.alu.execute(
                self.read_register(rs),
                self.read_register(rt),
                ALUOperation.SUB,
            )
            if difference != 0:
                next_pc += self.sign_extend(immediate)

        elif decoded.name == "andi":
            result = self.alu.execute(
                self.read_register(rs),
                immediate,
                ALUOperation.AND,
            )
            self.write_register(rt, result)

        else:
            raise ValueError(
                f"Unsupported instruction: {decoded.name}"
            )

        self.pc = next_pc
