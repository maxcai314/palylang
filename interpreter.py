import array
import re
import parser
from parser import Parser

MASK_32 = 0xFFFFFFFF
MASK_16 = 0xFFFF
MASK_8 = 0xFF
WORD_SIZE = 4  # 4 bytes for a 32-bit word

def to_signed_32(n):
    n = n & MASK_32
    return (n ^ 0x80000000) - 0x80000000

def to_signed_16(n):
    n = n & MASK_16
    return (n ^ 0x8000) - 0x8000

def to_signed_8(n):
    n = n & MASK_8
    return (n ^ 0x80) - 0x80

def trunc_divmod(a, b):
    q = int(a / b)
    r = a - b * q
    return (q, r)

# The VM has only these general-purpose registers
REGISTERS = [ "zero", "sp", "a0", "a1", "a2", "a3" ]

class RegisterFile:
    def __init__(self):
        self.regs = { reg: 0 for reg in REGISTERS }

    def read(self, reg):
        return self.regs[reg] & MASK_32

    def write(self, reg, val):
        if reg != "zero":
            self.regs[reg] = val & MASK_32

class VM:
    def __init__(self, mem_size = 1024):
        self.registers = RegisterFile()
        self.memory = array.array('B', [0] * mem_size)
        self.registers.write("sp", mem_size - 16)  # Initialize stack pointer
        self.code = None
        self.program_counter = 0xFFFFFFFF  # invalid initial PC
        self.label_locator = None  # function to locate labels

    def print_char(self, data):
        print(chr(data & MASK_8), end='')

    def load_word(self, address):
        if address % 4 != 0:
            raise ValueError("Unaligned memory access")
        word = (self.memory[address] |
                (self.memory[address + 1] << 8) |
                (self.memory[address + 2] << 16) |
                (self.memory[address + 3] << 24))
        return word & MASK_32
    
    def store_word(self, address, value):
        if address % 4 != 0:
            raise ValueError("Unaligned memory access")
        value &= MASK_32
        self.memory[address] = value & MASK_8
        self.memory[address + 1] = (value >> 8) & MASK_8
        self.memory[address + 2] = (value >> 16) & MASK_8
        self.memory[address + 3] = (value >> 24) & MASK_8
    
    def load_half(self, address):
        if address % 2 != 0:
            raise ValueError("Unaligned memory access")
        half = (self.memory[address] |
                (self.memory[address + 1] << 8))
        return to_signed_16(half)
    
    def load_half_unsigned(self, address):
        if address % 2 != 0:
            raise ValueError("Unaligned memory access")
        half = (self.memory[address] |
                (self.memory[address + 1] << 8))
        return half & MASK_16
    
    def store_half(self, address, value):
        if address % 2 != 0:
            raise ValueError("Unaligned memory access")
        self.memory[address] = value & MASK_8
        self.memory[address + 1] = (value >> 8) & MASK_8
    
    def load_byte(self, address):
        byte = self.memory[address]
        return to_signed_8(byte)
    
    def load_byte_unsigned(self, address):
        byte = self.memory[address]
        return byte & MASK_8
    
    def store_byte(self, address, value):
        self.memory[address] = value & MASK_8

    def load_program(self, parse_result: Parser):
        data_start = 256  # data segment starts at address 256

        data_labels = {}
        # Load data segment
        for i, word in enumerate(parse_result.data):
            self.store_word(data_start + i * WORD_SIZE, word)
        
        for label_idx, labels in enumerate(parse_result.data_labels):
            for label in labels:
                data_labels[label] = data_start + label_idx * WORD_SIZE

        def find_code_label(label, from_idx=None):
            # for int labels such as 0f or 0b, find the nearest matching label
            if re.match(r'^\d+$', label):
                raise ValueError("Numeric labels must specify direction with 'f' or 'b'")
            if re.match(r'^\d+[fb]$', label):
                if from_idx is None:
                    raise ValueError("from_idx must be provided for relative label search")
                target_name = label[:-1]
                direction = label[-1]
                if direction == 'f':  # forwards
                    for idx in range(from_idx + 1, len(parse_result.code_labels)):
                        if target_name in parse_result.code_labels[idx]:
                            return idx
                else:  # backwards
                    for idx in range(from_idx, -1, -1):
                        if target_name in parse_result.code_labels[idx]:
                            return idx
                raise ValueError(f"Label {label} not found")
            else:
                for idx, labels in enumerate(parse_result.code_labels):
                    if label in labels:
                        return idx
                raise ValueError(f"Label {label} not found")
        
        def label_locator_with(from_idx):
            def locator(label):
                return find_code_label(label, from_idx)
            return locator
        
        self.label_locator = find_code_label

        # Load code (separate memory)
        self.code = []
        for i, (instr, args) in enumerate(parse_result.code):
            # For simplicity, we will just store a lambda for each instruction
            # In a real VM, you would convert instructions to binary opcodes
            # Each instruction would be a function that takes the VM as an argument
            # https://www.cs.sfu.ca/~ashriram/Courses/CS295/assets/notebooks/RISCV/RISCV_CARD.pdf
            if instr == "nop":
                self.code.append(advance_pc)
            elif instr == "printc":
                self.code.append(make_printc(args))
            elif instr == "lw":
                self.code.append(make_load(args, VM.load_word))
            elif instr == "sw":
                self.code.append(make_store(args, VM.store_word))
            elif instr == "lh":
                self.code.append(make_load(args, VM.load_half))
            elif instr == "lhu":
                self.code.append(make_load(args, VM.load_half_unsigned))
            elif instr == "sh":
                self.code.append(make_store(args, VM.store_half))
            elif instr == "lb":
                self.code.append(make_load(args, VM.load_byte))
            elif instr == "lbu":
                self.code.append(make_load(args, VM.load_byte_unsigned))
            elif instr == "sb":
                self.code.append(make_store(args, VM.store_byte))
            elif instr == "la":
                self.code.append(make_load_addr(args, data_labels))
            elif instr == "add":
                self.code.append(make_binary_op(args, lambda x, y: x + y))
            elif instr == "addi":
                self.code.append(make_binary_opi(args, lambda x, y: x + y))
            elif instr == "sub":
                self.code.append(make_binary_op(args, lambda x, y: to_signed_32(x) - to_signed_32(y)))
            elif instr == "subi":
                self.code.append(make_binary_opi(args, lambda x, y: to_signed_32(x) - to_signed_32(y)))
            elif instr == "and":
                self.code.append(make_binary_op(args, lambda x, y: x & y))
            elif instr == "andi":
                self.code.append(make_binary_opi(args, lambda x, y: x & y))
            elif instr == "or":
                self.code.append(make_binary_op(args, lambda x, y: x | y))
            elif instr == "ori":
                self.code.append(make_binary_opi(args, lambda x, y: x | y))
            elif instr == "xor":
                if args == ["zero", "zero", "zero"]:
                    def debug_insn(vm):
                        print("\n--- DEBUG INSN HIT ---")
                        vm.dump_state()
                        print("----------------------\n")
                        advance_pc(vm)
                    # special case: xor zero, zero, zero is a debug insn
                    self.code.append(debug_insn)
                else:
                    self.code.append(make_binary_op(args, lambda x, y: x ^ y))
            elif instr == "xori":
                self.code.append(make_binary_opi(args, lambda x, y: x ^ y))
            elif instr == "sll":
                self.code.append(make_binary_op(args, lambda x, y: (x << y) & MASK_32))
            elif instr == "slli":
                self.code.append(make_binary_opi(args, lambda x, y: (x << y) & MASK_32))
            elif instr == "srl":
                self.code.append(make_binary_op(args, lambda x, y: (x & MASK_32) >> y))
            elif instr == "srli":
                self.code.append(make_binary_opi(args, lambda x, y: (x & MASK_32) >> y))
            elif instr == "sra":
                self.code.append(make_binary_op(args, lambda x, y: to_signed_32(x) >> y))
            elif instr == "srai":
                self.code.append(make_binary_opi(args, lambda x, y: to_signed_32(x) >> y))
            elif instr == "slt":
                self.code.append(make_binary_op(args, lambda x, y: 1 if to_signed_32(x) < to_signed_32(y) else 0))
            elif instr == "slti":
                self.code.append(make_binary_opi(args, lambda x, y: 1 if to_signed_32(x) < to_signed_32(y) else 0))
            elif instr == "sltu":
                self.code.append(make_binary_op(args, lambda x, y: 1 if (x & MASK_32) < (y & MASK_32) else 0))
            elif instr == "sltui":
                self.code.append(make_binary_opi(args, lambda x, y: 1 if (x & MASK_32) < (y & MASK_32) else 0))
            elif instr == "beq":
                self.code.append(make_branch_op(args, label_locator_with(i), lambda x, y: x == y))
            elif instr == "bne":
                self.code.append(make_branch_op(args, label_locator_with(i), lambda x, y: x != y))
            elif instr == "blt":
                self.code.append(make_branch_op(args, label_locator_with(i), lambda x, y: to_signed_32(x) < to_signed_32(y)))
            elif instr == "bge":
                self.code.append(make_branch_op(args, label_locator_with(i), lambda x, y: to_signed_32(x) >= to_signed_32(y)))
            elif instr == "bltu":
                self.code.append(make_branch_op(args, label_locator_with(i), lambda x, y: (x & MASK_32) < (y & MASK_32)))
            elif instr == "bgeu":
                self.code.append(make_branch_op(args, label_locator_with(i), lambda x, y: (x & MASK_32) >= (y & MASK_32)))
            elif instr == "jalr":
                self.code.append(make_jalr(args))
            elif instr == "jal":
                self.code.append(make_jal(args, label_locator_with(i)))
            elif instr == "mul":
                self.code.append(make_binary_op(args, lambda x, y: to_signed_32(x) * to_signed_32(y)))
            elif instr == "mulh":
                self.code.append(make_binary_op(args, lambda x, y: (to_signed_32(x) * to_signed_32(y)) >> 32))
            elif instr == "mulhu":
                self.code.append(make_binary_op(args, lambda x, y: ((x & MASK_32) * (y & MASK_32)) >> 32))
            elif instr == "div":
                self.code.append(make_binary_op(args, lambda x, y: trunc_divmod(to_signed_32(x), to_signed_32(y))[0] if y != 0 else 0xFFFFFFFF))
            elif instr == "divu":
                self.code.append(make_binary_op(args, lambda x, y: (x & MASK_32) // (y & MASK_32) if y != 0 else 0xFFFFFFFF))
            elif instr == "rem":
                self.code.append(make_binary_op(args, lambda x, y: trunc_divmod(to_signed_32(x), to_signed_32(y))[1] if y != 0 else 0xFFFFFFFF))
            elif instr == "remu":
                self.code.append(make_binary_op(args, lambda x, y: (x & MASK_32) % (y & MASK_32) if y != 0 else 0xFFFFFFFF))
            else:
                raise ValueError(f"Unknown instruction: {instr}")

    def interpret_step(self) -> bool:
        # Returns whether is halted
        # keep running this until it returns True
        if self.code is None:
            raise ValueError("No program loaded")

        if self.program_counter == 0xFFFFFFFF:
            return True  # halted
        
        if self.program_counter < 0 or self.program_counter >= len(self.code):
            raise ValueError("Program counter out of bounds")
        
        instr = self.code[self.program_counter]
        instr(self)  # execute instruction
        return False  # not halted
    
    def call_function(self, function_label):
        # sets the VM to call a function at addr
        # should only be called when halted
        addr = self.label_locator(function_label)

        self.registers.write("ra", self.program_counter)
        self.program_counter = addr
    
    def dump_state(self):
        print("Registers:")
        for reg in REGISTERS:
            print(f"  {reg}: {hex(self.registers.read(reg))} ({to_signed_32(self.registers.read(reg))})")
        if self.program_counter == 0xFFFFFFFF:
            print("Program Counter: HALTED")
        else:
            print(f"Program Counter: {hex(self.program_counter)} ({self.program_counter})")

def advance_pc(vm):
    vm.program_counter += 1

def make_printc(args):
    dest_reg = args[0]
    def printc_instr(vm):
        vm.print_char(vm.registers.read(dest_reg))
        advance_pc(vm)
    return printc_instr

def make_load(args, method_handle):
    # example: lw a1, 4(a3)
    dest_reg = args[0]
    pattern = r'(-?\d+)\((\w+)\)'
    match = re.match(pattern, args[1])
    if not match:
        raise ValueError("Invalid address format for lw")
    offset = int(match.group(1), 0)
    base_reg = match.group(2)
    def load_instr(vm):
        addr = (vm.registers.read(base_reg) + offset) & MASK_32
        val = method_handle(vm, addr) & MASK_32
        vm.registers.write(dest_reg, val)
        advance_pc(vm)
    return load_instr

def make_store(args, method_handle):
    # example: sw 0(sp), a0
    pattern = r'(-?\d+)\((\w+)\)'
    match = re.match(pattern, args[0])
    if not match:
        raise ValueError("Invalid address format for sw")
    offset = int(match.group(1), 0)
    base_reg = match.group(2)
    src_reg = args[1]
    def store_instr(vm):
        addr = (vm.registers.read(base_reg) + offset) & MASK_32
        val = vm.registers.read(src_reg) & MASK_32
        method_handle(vm, addr, val)
        advance_pc(vm)
    return store_instr

def make_load_addr(args, data_labels):
    # example: la a0, my_label
    dest_reg = args[0]
    label = args[1]
    if label not in data_labels:
        raise ValueError(f"Label '{label}' not found")
    address = data_labels[label]
    def load_addr_instr(vm):
        vm.registers.write(dest_reg, address)
        advance_pc(vm)
    return load_addr_instr

def make_binary_op(args, op_func):
    # example: add a0, a1, a2
    dest_reg = args[0]
    src_reg1 = args[1]
    src_reg2 = args[2]
    def binary_op_instr(vm):
        val = op_func(vm.registers.read(src_reg1), vm.registers.read(src_reg2)) & MASK_32
        vm.registers.write(dest_reg, val)
        advance_pc(vm)
    return binary_op_instr

def make_binary_opi(args, op_func):
    # example: addi a0, a1, 10
    dest_reg = args[0]
    src_reg = args[1]
    immediate = int(args[2], 0)
    def binary_opi_instr(vm):
        val = op_func(vm.registers.read(src_reg), immediate) & MASK_32
        vm.registers.write(dest_reg, val)
        advance_pc(vm)
    return binary_opi_instr

def make_branch_op(args, find_label_func, condition_func):
    # example: beq a0, a1, label
    src_reg1 = args[0]
    src_reg2 = args[1]
    target = find_label_func(args[2])
    def branch_op_instr(vm):
        if condition_func(vm.registers.read(src_reg1), vm.registers.read(src_reg2)):
            vm.program_counter = target
        else:
            advance_pc(vm)
    return branch_op_instr

def make_jalr(args):
    # example: jalr zero, ra, 0
    # that third argument is optional
    dest_reg = args[0]
    base_reg = args[1]
    target_offset = int(args[2] if len(args) > 2 else "0", 0)
    def jalr_instr(vm):
        return_address = vm.program_counter + 1
        target_address = (vm.registers.read(base_reg) + target_offset) & MASK_32
        vm.registers.write(dest_reg, return_address)
        vm.program_counter = target_address
    return jalr_instr

def make_jal(args, find_label_func):
    # example: jal ra, label
    dest_reg = args[0]
    target = find_label_func(args[1])
    def jal_instr(vm):
        return_address = vm.program_counter + 1
        vm.registers.write(dest_reg, return_address)
        vm.program_counter = target
    return jal_instr

if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        print("Please enter the name of the asm file to run")
        sys.exit(1)

    filename = sys.argv[1]
    asm_parser = parser.parse_file(filename)

    vm = VM(mem_size=1024)
    vm.load_program(asm_parser)

    target_function = sys.argv[2] if len(sys.argv) > 2 else "main"
    vm.call_function(target_function)

    verbose = "--verbose" in sys.argv[1:]
    def debug_dump(vm):
        if verbose:
            vm.dump_state()
    
    def debug_print(msg):
        if verbose:
            print(msg)

    if verbose:
        print("ASM Dump:\n")
        parser.dump_asm(asm_parser)
        print("\n")

    debug_print(f"Calling function '{target_function}'...\n")
    debug_print("\nStarting VM execution...\n")

    debug_dump(vm)
    pre_sp = vm.registers.read("sp")

    try:
        while not vm.interpret_step():
            debug_dump(vm)
            # pass
    except Exception as e:
        print(f"\nError during execution: {e}")
        vm.dump_state()
        raise e

    debug_dump(vm)

    debug_print("Done! VM halted.")

    post_sp = vm.registers.read("sp")
    if pre_sp != post_sp:
        print(f"\nWarning: Stack pointer changed from {hex(pre_sp)} to {hex(post_sp)}")
