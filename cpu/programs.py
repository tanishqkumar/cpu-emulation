# # Example program: Add two numbers (e.g., 7 + 5) and halt.
# # This runs: ACC = 7; ACC = ACC + 5; HALT

# add_two_numbers_program = [
#     0x01, 0x07,   # LDI 7      (ACC = 7)
#     0x10, 0x0A,   # ADD 0x0A   (ACC = ACC + MEM[0x0A])
#     0xFF,         # HALT
#     # --- Data section (address 0x0A) ---
#     # We'll store the value 5 at memory address 0x0A.
# ] + [0] * (0x0A - 5) + [0x05]  # 0x05 at 0x0A

# # To run: cpu.load_program(add_two_numbers_program); cpu.run()
# # The result (sum) will be in the ACC register (should be 12 for 7+5).

add_two_numbers_program = [
    0x1,
    0x2,
    0x3,
    0x1,
    0x1,
    0x5,
    0x3,
    0x2,
    0x2,
    0x1,
    0x10,
    0x2,
    0x3,
    0x0,
    0x1,
    0x3,
    0x10,
    0x0,
    0x3,
    0x3,
    0x2,
    0x3,
    0x3,
    0x0,
    0x1,
    0xb,
    0x10,
    0x0,
    0xff,
]