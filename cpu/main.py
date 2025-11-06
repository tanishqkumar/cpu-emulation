import sys
from pathlib import Path

# Add project root to path for proper package imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
print(f"Running from: {__file__}")
print(f"Project root: {project_root}")


from cpu import CPU
from compile import compile, assemble
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minimal 8-bit CPU runner")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose tracing")
    parser.add_argument("--mem", type=int, default=256, help="Memory size (must be multiple of 16)")
    parser.add_argument("--program", type=str, default="program.txt", help="Path to program file")
    args = parser.parse_args()
    assert args.mem % 16 == 0, f"Memory size must be a multiple of 16, got {args.mem}"
    
    # Compile and assemble the program
    compiled_program = compile(args.program)
    print(f"Compiled {len(compiled_program)} instructions")
    
    print("Assembling program...")
    assembled_program = assemble(compiled_program)
    print(f"Assembled {len(assembled_program)} bytes")
    
    # Run the program
    cpu = CPU(mem_sz=args.mem, verbose=args.verbose)
    cpu.load_program(assembled_program)
    cpu.run()
    print(f'--------------------------------')
    print(f'Final Result: {cpu.control_unit.registers["ACC"]}')
    print(f'--------------------------------')