OPCODES = { 
    0x00: "NOP",   # 0x00: No operation (do nothing)
    0x01: "LDI",   # 0x01: Load immediate value into ACC (ACC = imm)
    0x02: "LDA",   # 0x02: Load from memory at address into ACC (ACC = MEM[addr])
    0x03: "STA",   # 0x03: Store ACC into memory at address (MEM[addr] = ACC)
    0x10: "ADD",   # 0x10: Add memory at address to ACC (ACC = ACC + MEM[addr])
    0x11: "SUB",   # 0x11: Subtract memory at address from ACC (ACC = ACC - MEM[addr])
    0x12: "AND",   # 0x12: Bitwise AND memory at address with ACC (ACC = ACC & MEM[addr])
    0x13: "OR",    # 0x13: Bitwise OR memory at address with ACC (ACC = ACC | MEM[addr])
    0x14: "XOR",   # 0x14: Bitwise XOR memory at address with ACC (ACC = ACC ^ MEM[addr])
    0x15: "NOT",   # 0x15: Bitwise NOT of ACC (ACC = ~ACC, masked to 8 bits)
    0x20: "JMP",   # 0x20: Unconditional jump to address (IP = addr)
    0x21: "JZ",    # 0x21: Jump if zero flag (Z) set (if Z: IP = addr)
    0x22: "JNZ",   # 0x22: Jump if zero flag not set (if not Z: IP = addr)
    0xFF: "HALT",  # 0xFF: Halt execution
}

# Example of tuple-based program as produced by compile_from_ast.py:
example_tuple_program = [
    ("LDI", 2),
    ("STA", 0x1),
    ("LDI", 5),
    ("STA", 0x2),
    ("LDA", 0x1),
    ("ADD", 0x2),
    ("STA", 0x0),
    ("LDI", 3),
    ("ADD", 0x0),
    ("STA", 0x3),
    ("LDA", 0x3),
    ("STA", 0x0),
    ("LDI", 11),
    ("ADD", 0x0),
    ("HALT",)
]

def assemble(program: list[tuple]) -> list[int]:
    """
    Assemble a list of tuples of op/arg as emitted by the compiler.
    Each element is a tuple: ("OP", arg) or just ("OP",)
    """
    CODEOPS = {v: k for k, v in OPCODES.items()}
    out = []
    for instr in program:
        match instr:
            case (op, arg):  # two elements
                codeop = CODEOPS[op]
                out.append(codeop)
                # Supports hex string args like '0xA1', or already-int
                if isinstance(arg, str) and arg.startswith('0x'):
                    out.append(int(arg, 16))
                else:
                    out.append(int(arg))
            case (op,):      # just ("HALT",), etc
                codeop = CODEOPS[op]
                out.append(codeop)
            case _:
                raise ValueError(f"Invalid instruction tuple: {instr}")
    return out

if __name__ == "__main__":
    out = assemble(example_tuple_program)
    for line in out:
        print(line)