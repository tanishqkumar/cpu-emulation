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

example_program = [
    "LDI 2",
    "STA 0x1",
    "LDI 5",
    "STA 0x2",
    "LDA 0x1",
    "ADD 0x2",
    "STA 0x0",
    "LDI 3",
    "ADD 0x0",
    "STA 0x3",
    "LDA 0x3",
    "STA 0x0",
    "LDI 11",
    "ADD 0x0",
    "HALT"
]

def assemble(program: list[str]) -> list[int]:
    CODEOPS = {v: k for k, v in OPCODES.items()}
    out = []
    for line in program: 
        args = line.split(" ")
        assert len(args) in [1, 2], "Invalid instruction"
        CODEOP = CODEOPS[args[0]]
        out.append(CODEOP)
        if len(args) > 1: 
            out.append(eval(args[1]))

    return out 

if __name__ == "__main__":
    out = assemble(example_program)
    for line in out:
        print(line)