# To get started:
# - Implement the ALU first: a class with a method to perform add/sub/and/or/xor/not on 8-bit values, updating a zero flag as needed.
# - Build a simple Memory class: a 256-byte array with read/write/load methods.
# - Design the ControlUnit: handles registers (IP, ACC, Z), fetches and decodes instructions, and uses the ALU and Memory.
# - The CPU class ties them all together and provides convenience methods for loading and running programs.
# - Start by supporting core instructions: LDI, LDA, STA, ADD, SUB, JMP, JZ, JNZ, HALT.
# - Test with simple sample programs (see programs.py).
from .handlers import OPCODES, OPCODE_ARGCOUNTS, HANDLERS
from .utils import print_state 

class ALU: 
    def operate(self, op: str, a: int, b: int | None = None) -> tuple[int, dict]: 
        """Return (result, flags). flags includes {'Z': bool}. Values masked to 0..255."""
        if op == "add":
            result = (a + b) % 256
        elif op == "sub":
            result = (a - b) % 256
        elif op == "and":
            result = a & b
        elif op == "or":
            result = a | b
        elif op == "xor":
            result = a ^ b
        elif op == "not":
            result = (~a) & 0xFF
        else: 
            raise NotImplementedError(f"Operation {op} not implemented")
        return result, {"Z": result == 0, "N": result < 0}

class Memory:
    def __init__(self, size: int = 256):
        self.memory = [0] * size

    def __len__(self) -> int: 
        return len(self.memory)

    def __getitem__(self, addr: int) -> int:
        return self.memory[addr]
    
    def __setitem__(self, addr: int, value: int) -> None:
        self.memory[addr] = value

    def read(self, addr: int) -> int:
        return self.memory[addr]

    def write(self, addr: int, value: int) -> None:
        self.memory[addr] = value

    def load_bytes(self, bytes_: list[int], at: int = 0) -> None: 
        # used to load programs into memory at beginning of execution
        for i, byte in enumerate(bytes_):
            self.memory[at + i] = byte

class ControlUnit: 
    def __init__(self, memory: Memory, alu: ALU):
        self.memory = memory
        self.alu = alu
        self.registers = {
            "IP": 0,
            "ACC": 0,
        }
        self.flags = {"Z": False, "N": False}

    def update_ip(self, opcode_byte: int) -> None: 
        self.registers["IP"] += OPCODE_ARGCOUNTS[opcode_byte] + 1
    
    def fetch(self) -> int: 
        opcode = self.memory.read(self.registers["IP"])
        if not opcode in OPCODES:
            raise ValueError(f"Invalid opcode: {opcode}")
        return opcode

    def decode(self, opcode: int) -> str: 
        return OPCODES[opcode]

    def execute(self, opcode_name: str) -> tuple[bool, dict, bool]: 
        return HANDLERS[opcode_name](self)
    
    def clock_cycle(self) -> bool: # (memory, instruction ptr) -> memory', instruction ptr'
        """Execute one instruction. Return False on HALT, True otherwise."""
        opcode = self.fetch()
        opcode_name = self.decode(opcode)
        contin, flags, touched_ip = self.execute(opcode_name)
        
        if flags is not None: 
            self.flags["Z"] = flags["Z"]
            self.flags["N"] = flags["N"]
        
        if not contin:
            return False
        
        if not touched_ip:
            self.update_ip(opcode)
        
        return True
        
class CPU: 
    def __init__(self, mem_sz: int = 256, verbose: bool = False): 
        self.mem_sz = mem_sz
        self.memory = Memory(mem_sz)
        self.alu = ALU()
        self.control_unit = ControlUnit(self.memory, self.alu)
        self.verbose = verbose

    def load_program(self, program: list[int]) -> None:
        if len(program) > len(self.memory):
            raise ValueError(f"Program is too large for memory")
        self.memory.load_bytes(program)

    def run(self, max_steps: int = 10_000) -> None:
        step = 0 
        while step < max_steps:
            if self.verbose:
                print_state(self, step)
            if not self.control_unit.clock_cycle():
                break
            step += 1
        return self.control_unit.registers["ACC"]