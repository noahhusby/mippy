
"""Main entry point for the MIPS CPU simulator."""

from assembler import assemble
from cpu import CPU


PROGRAM = """
    # Load values from data memory
    lw   $t0, 100($zero)
    lw   $t1, 101($zero)

    # Add the two values
    add  $t2, $t0, $t1

    # Apply a bitwise mask
    andi $t3, $t2, 0x000F

    # Store the result
    sw   $t3, 102($zero)

    # Test BEQ: branch is taken
    beq  $t0, $t0, equal

    # Skipped when BEQ is taken
    add  $t4, $t0, $t1

equal:
    # Test BNE: branch is taken
    bne  $t0, $t1, done

    # Skipped when BNE is taken
    add  $t5, $t0, $t1

done:
"""


def main() -> None:
    cpu = CPU()
    instructions = assemble(PROGRAM)

    # Initialize sample data
    cpu.data_memory.write(100, 10)
    cpu.data_memory.write(101, 20)

    # Load machine code into instruction memory
    cpu.instruction_memory.load(instructions)

    print("MIPS CPU Simulation")
    print("=" * 60)

    print("\nAssembled instructions:")
    for address, instruction in enumerate(instructions):
        print(f"{address:04d}: 0x{instruction:08X}")

    print("\nExecution:")
    cycle = 0

    # Execute until PC leaves the loaded program.
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

    print("\nFinal register state:")
    cpu.registers.dump()

    print("\nData memory:")
    cpu.data_memory.dump(100, 3)

    # Verify expected results
    assert cpu.registers.read(8) == 10
    assert cpu.registers.read(9) == 20
    assert cpu.registers.read(10) == 30
    assert cpu.registers.read(11) == 14
    assert cpu.registers.read(12) == 0
    assert cpu.registers.read(13) == 0
    assert cpu.data_memory.read(102) == 14

    print(f"\nSimulation completed in {cycle} cycles.")
    print("All result checks passed.")


if __name__ == "__main__":
    main()
