# OPCODES dictionary: maps each opcode byte to its instruction mnemonic (tldr: what the instruction is)
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



# OPCODE_ARGCOUNTS dictionary: maps opcode byte to # of arguments (tldr: how many bytes after opcode?)
OPCODE_ARGCOUNTS = {
    0x00: 0,  # NOP: no operand
    0x01: 1,  # LDI imm: loads immediate byte
    0x02: 1,  # LDA addr: loads from this memory address
    0x03: 1,  # STA addr: stores ACC at this memory address
    0x10: 1,  # ADD addr: add ACC + value at this memory address
    0x11: 1,  # SUB addr: subtract value at this memory address from ACC
    0x12: 1,  # AND addr: ACC = ACC & MEM[addr]
    0x13: 1,  # OR addr: ACC = ACC | MEM[addr]
    0x14: 1,  # XOR addr: ACC = ACC ^ MEM[addr]
    0x15: 0,  # NOT: ACC = ~ACC (no operand)
    0x20: 1,  # JMP addr: jump to this address
    0x21: 1,  # JZ addr: jump if Z flag set
    0x22: 1,  # JNZ addr: jump if not Z flag set
    0xFF: 0,  # HALT: no operand
}

# Only ALU-type instructions return flags; others return None.
def handle_nop(control_unit):
    return True, None, False

def handle_ldi(control_unit):
    ip = control_unit.registers["IP"]
    imm = control_unit.memory.read(ip + 1)
    control_unit.registers["ACC"] = imm
    return True, None, False

def handle_lda(control_unit):
    ip = control_unit.registers["IP"]
    addr = control_unit.memory.read(ip + 1)
    control_unit.registers["ACC"] = control_unit.memory.read(addr)
    return True, None, False

def handle_sta(control_unit):
    ip = control_unit.registers["IP"]
    addr = control_unit.memory.read(ip + 1)
    control_unit.memory.write(addr, control_unit.registers["ACC"])
    return True, None, False

def handle_add(control_unit):
    ip = control_unit.registers["IP"]
    addr = control_unit.memory.read(ip + 1)
    curr_val = control_unit.registers["ACC"]
    to_add = control_unit.memory.read(addr)
    result, flags = control_unit.alu.operate("add", curr_val, to_add)
    control_unit.registers["ACC"] = result
    return True, flags, False

def handle_sub(control_unit):
    ip = control_unit.registers["IP"]
    addr = control_unit.memory.read(ip + 1)
    curr_val = control_unit.registers["ACC"]
    to_sub = control_unit.memory.read(addr)
    result, flags = control_unit.alu.operate("sub", curr_val, to_sub)
    control_unit.registers["ACC"] = result
    return True, flags, False

def handle_and(control_unit):
    ip = control_unit.registers["IP"]
    addr = control_unit.memory.read(ip + 1)
    curr_val = control_unit.registers["ACC"]
    to_and = control_unit.memory.read(addr)
    result, flags = control_unit.alu.operate("and", curr_val, to_and)
    control_unit.registers["ACC"] = result
    return True, flags, False

def handle_or(control_unit):
    ip = control_unit.registers["IP"]
    addr = control_unit.memory.read(ip + 1)
    curr_val = control_unit.registers["ACC"]
    to_or = control_unit.memory.read(addr)
    result, flags = control_unit.alu.operate("or", curr_val, to_or)
    control_unit.registers["ACC"] = result
    return True, flags, False

def handle_xor(control_unit):
    ip = control_unit.registers["IP"]
    addr = control_unit.memory.read(ip + 1)
    curr_val = control_unit.registers["ACC"]
    to_xor = control_unit.memory.read(addr)
    result, flags = control_unit.alu.operate("xor", curr_val, to_xor)
    control_unit.registers["ACC"] = result
    return True, flags, False

def handle_not(control_unit):
    curr_val = control_unit.registers["ACC"]
    result, flags = control_unit.alu.operate("not", curr_val)
    control_unit.registers["ACC"] = result
    return True, flags, False

def handle_jmp(control_unit):
    ip = control_unit.registers["IP"]
    addr = control_unit.memory.read(ip + 1)
    control_unit.registers["IP"] = addr
    return True, None, True

def handle_jz(control_unit):
    ip = control_unit.registers["IP"]
    addr = control_unit.memory.read(ip + 1)
    if control_unit.flags.get("Z", False):
        control_unit.registers["IP"] = addr
    else:
        control_unit.registers["IP"] += 2  # Skip opcode and operand
    return True, None, True

def handle_jnz(control_unit):
    ip = control_unit.registers["IP"]
    addr = control_unit.memory.read(ip + 1)
    if not control_unit.flags.get("Z", False):
        control_unit.registers["IP"] = addr
    else:
        control_unit.registers["IP"] += 2  # Skip opcode and operand
    return True, None, True

def handle_halt(control_unit):
    return False, None, False

HANDLERS = {
    "NOP": handle_nop,
    "LDI": handle_ldi,
    "LDA": handle_lda,
    "STA": handle_sta,
    "ADD": handle_add,
    "SUB": handle_sub,
    "AND": handle_and,
    "OR": handle_or,
    "XOR": handle_xor,
    "NOT": handle_not,
    "JMP": handle_jmp,
    "JZ": handle_jz,
    "JNZ": handle_jnz,
    "HALT": handle_halt,
}