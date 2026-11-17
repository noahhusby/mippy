
"""
ECE 485 - MIPS Single-Cycle CPU
Author: Noah Husby
File: main.py
Description: CPU simulation entry point and sample program.
"""
from assembler import assemble
from cpu import CPU

def _run_sim(cpu: CPU, instructions: list[int]) -> None:
    print("\nRunning simulation...:")

    cycle = 0
    while 0 <= cpu.pc < len(instructions):
        current_pc = cpu.pc
        instruction = cpu.instruction_memory.read(current_pc)

        print(
            f"Cycle {cycle + 1:02d} | "
            f"PC={current_pc:04d} | "
            f"Instruction=0x{instruction:08X}"
        )

        cpu.execute(instruction)
        cycle += 1

        # Guard against accidental infinite loops.
        if cycle >= 100:
            raise RuntimeError("Maximum cycle count exceeded")

    print("\nFinal register state (only non-zero registers shown):")
    print(cpu.registers)
    print("\nData memory (only non-zero memory values shown):")
    print(cpu.data_memory)


    print(f"\nSimulation completed in {cycle} cycles.")


def _test_lw() -> None:
    """Test the specified load word command."""
    program = "lw $t3, 300($s2)"
    print("\n------------------\nRunning simulation for program:\n" + program)
    cpu = CPU()

    cpu.registers.write(18, 100)   # $s2
    cpu.data_memory.write(400, 75)

    instructions = assemble(program)
    cpu.instruction_memory.load(instructions)

    _run_sim(cpu, instructions)

    assert cpu.registers.read(11) == 75
    assert cpu.registers.read(18) == 100
    assert cpu.data_memory.read(400) == 75
    assert cpu.pc == 1

def _test_sw() -> None:
    """Test the specified store word command."""
    program = "sw $t6, 400($s7)"
    print("\n------------------\nRunning simulation for program:\n" + program)
    cpu = CPU()

    cpu.registers.write(23, 100)  # $s7
    cpu.registers.write(14, 75)   # $t6

    instructions = assemble(program)
    cpu.instruction_memory.load(instructions)

    _run_sim(cpu, instructions)

    assert cpu.data_memory.read(500) == 75
    assert cpu.registers.read(14) == 75
    assert cpu.registers.read(23) == 100
    assert cpu.pc == 1

def _test_add() -> None:
    """Test the specified add command."""
    program = "add $t5, $t3, $s1"
    print("\n------------------\nRunning simulation for program:\n" + program)
    cpu = CPU()

    cpu.registers.write(11, 25)  # $t3
    cpu.registers.write(17, 50)  # $s1

    instructions = assemble(program)
    cpu.instruction_memory.load(instructions)

    _run_sim(cpu, instructions)

    assert cpu.registers.read(13) == 75  # $t5
    assert cpu.registers.read(11) == 25
    assert cpu.registers.read(17) == 50
    assert cpu.pc == 1

def _test_bne() -> None:
    """Test the specified branch not equal command."""
    program = """
    bne $s6, $t5, 200
    add $t0, $s6, $t5
    """

    print("\n------------------\nRunning simulation for program:\n" + program)
    cpu = CPU()

    cpu.registers.write(22, 10)  # $s6
    cpu.registers.write(13, 10)  # $t5

    instructions = assemble(program)
    cpu.instruction_memory.load(instructions)

    _run_sim(cpu, instructions)

    assert cpu.registers.read(8) == 20
    assert cpu.pc == 2

def _test_beq() -> None:
    """Test the branch equal command."""
    program = "\n".join([
        "beq $t0, $t1, 1",
        "andi $t2, $zero, 1",
        "andi $t3, $t0, 15",
    ])

    print("\n------------------\nRunning simulation for program:\n" + program)
    cpu = CPU()

    cpu.registers.write(8, 25)  # $t0
    cpu.registers.write(9, 25)  # $t1

    instructions = assemble(program)
    cpu.instruction_memory.load(instructions)

    _run_sim(cpu, instructions)

    assert cpu.registers.read(10) == 0   # $t2 skipped
    assert cpu.registers.read(11) == 9   # 25 & 15 = 9
    assert cpu.pc == 3

def _test_andi() -> None:
    """Test the AND immediate command."""
    program = "andi $t1, $t0, 15"
    print("\n------------------\nRunning simulation for program:\n" + program)
    cpu = CPU()

    cpu.registers.write(8, 42)  # $t0

    instructions = assemble(program)
    cpu.instruction_memory.load(instructions)

    _run_sim(cpu, instructions)

    assert cpu.registers.read(9) == 10  # $t1
    assert cpu.registers.read(8) == 42
    assert cpu.pc == 1

def _test_combined() -> None:
    """Test multiple instructions executing together."""
    program = """
    lw $t0, 10($s0)
    add $t1, $t0, $t0
    sw $t1, 20($s0)
    bne $t0, $t1, 1
    andi $t2, $t1, 15
    beq $t0, $t0, 1
    add $t3, $t0, $t1
    lw $t4, 20($s0)
    """

    print("\n------------------\nRunning simulation for program:\n" + program)
    cpu = CPU()

    cpu.registers.write(16, 100)  # $s0
    cpu.data_memory.write(110, 25)

    instructions = assemble(program)
    cpu.instruction_memory.load(instructions)

    _run_sim(cpu, instructions)

    assert cpu.registers.read(8) == 25    # $t0: loaded value
    assert cpu.registers.read(9) == 50    # $t1: addition result
    assert cpu.registers.read(10) == 0    # $t2: skipped by BNE
    assert cpu.registers.read(11) == 0    # $t3: skipped by BEQ
    assert cpu.registers.read(12) == 50   # $t4: loaded stored value
    assert cpu.data_memory.read(120) == 50
    assert cpu.pc == 8

def main() -> None:
    print("Mippy Simulation Suite - Noah Husby")
    _test_lw()
    _test_sw()
    _test_add()
    _test_bne()
    _test_beq()
    _test_andi()
    _test_combined()


if __name__ == "__main__":
    main()