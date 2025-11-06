
def print_state(cpu, step):
    print("---")
    print(f"Step {step}")
    print(f"  IP : {cpu.control_unit.registers['IP']}")
    print(f"  ACC: {cpu.control_unit.registers['ACC']}")
    print(f"  Z  : {cpu.control_unit.flags['Z']}")
    # Print memory as a grid (16 bytes per row, hex format)
    mem = cpu.memory
    row_sz = 16
    total = len(mem)
    print("  Memory:")
    for i in range(0, total, row_sz):
        chunk = mem[i:i+row_sz]
        addr_label = f"{i:02X}:"
        bytes_str = " ".join(f"{b:02X}" for b in chunk)
        print(f"   {addr_label} {bytes_str}")

