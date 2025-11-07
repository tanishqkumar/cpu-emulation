# CPU Emulator

A minimal 8-bit CPU emulator with a custom instruction set, compiler, and assembler. Write programs in a simple high-level language and execute them on an emulated CPU.

## Overview

This project implements a complete software stack for an 8-bit CPU:

- **CPU Emulator**: Simulates an 8-bit accumulator-based CPU with ALU, memory, and control unit
- **Compiler**: Translates high-level code into assembly instructions
- **Assembler**: Converts assembly instructions into executable bytecode

## Architecture

### CPU Components
- **ALU**: Performs arithmetic and logic operations (add, sub, and, or, xor, not)
- **Memory**: 256 bytes of RAM (configurable)
- **Control Unit**: Manages instruction fetch-decode-execute cycle
- **Registers**: 
  - `ACC`: Accumulator register for arithmetic operations
  - `IP`: Instruction pointer
- **Flags**: Zero flag (Z), Negative flag (N)

## Usage

### Running a Program

```bash
python cpu/main.py 
```

Options:
- `--program`: Path to the program file (default: `program.txt`)
- `--verbose`: Enable verbose execution tracing
- `--mem`: Memory size in bytes, must be multiple of 16 (default: 256)

### Writing Programs

Programs are written in a simple high-level language featuring:

- Variable assignment
- While loops
- Arithmetic operations
- Conditional expressions

#### Examples

```
x = 0
y = 2
while x != 5
    x = x + 1
endwhile
return x
```

```
x = 2
y = 5
z = x + y + 3
return z
```

These programs are compiled to assembly, assembled into bytecode, and executed on the CPU emulator, with the result available in the accumulator register.


## Project Structure

```
cpu/
├── compile/          # Compiler and assembler
│   ├── lex.py       # Lexer
│   ├── parse.py     # Parser
│   ├── ast_types.py # AST definitions
│   ├── compile_from_ast.py  # Code generation
│   └── assemble.py  # Bytecode assembler
├── cpu/             # CPU emulator
│   ├── cpu.py       # CPU, ALU, Memory, Control Unit
│   ├── handlers.py  # Instruction handlers
│   └── main.py      # Entry point
└── README.md
```

## Future Work

- Register-based architecture extensions
- Pipelining
- Speculative execution
- Out-of-order execution
- Branch prediction
