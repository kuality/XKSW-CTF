import sys
import pathlib

# VM Opcodes
opcodes = {
    0x00: ("HALT", 0),
    0x01: ("PUSH_IMM8", 1),
    0x02: ("PUSH_IMM16", 2),
    0x03: ("POP", 0),
    0x04: ("DUP", 0),
    0x05: ("SWAP", 0),
    
    0x10: ("ADD", 0),
    0x11: ("SUB", 0),
    0x12: ("MUL", 0),
    0x13: ("MOD", 0),
    0x14: ("XOR", 0),
    0x15: ("AND", 0),
    0x16: ("OR", 0),
    0x17: ("NOT", 0),
    0x18: ("ROL", 0),
    0x19: ("ROR", 0),
    
    0x20: ("LOAD", 0),
    0x21: ("STORE", 0),
    0x22: ("LOAD_IND", 0),
    
    0x30: ("JMP", 2),
    0x31: ("JZ", 2),
    0x32: ("JNZ", 2),
    0x33: ("JEQ", 2),
    
    0x40: ("READ", 0),
    0x41: ("WRITE", 0),
    
    0x50: ("CALL", 2),
    0x51: ("RET", 0),
}

def disassemble(bytecode, start=0, length=None):
    if length is None:
        length = len(bytecode)
    
    instructions = []
    pc = start
    end = min(start + length, len(bytecode))
    
    while pc < end:
        addr = pc
        op = bytecode[pc]
        pc += 1
        
        if op not in opcodes:
            instructions.append((addr, f"DB 0x{op:02x}", None))
            continue
        
        mnemonic, arg_count = opcodes[op]
        args = []
        
        if arg_count > 0:
            if pc + arg_count > len(bytecode):
                instructions.append((addr, f"{mnemonic} <incomplete>", None))
                break
            
            if arg_count == 1:
                args.append(bytecode[pc])
                pc += 1
            elif arg_count == 2:
                # Little-endian 16-bit value
                val = bytecode[pc] | (bytecode[pc + 1] << 8)
                args.append(val)
                pc += 2
        
        instructions.append((addr, mnemonic, args))
    
    return instructions

def format_instruction(addr, mnemonic, args):
    if args is None:
        return f"{addr:04x}: {mnemonic}"
    elif not args:
        return f"{addr:04x}: {mnemonic}"
    elif len(args) == 1:
        if mnemonic in ["JMP", "JZ", "JNZ", "JEQ", "CALL"]:
            return f"{addr:04x}: {mnemonic} 0x{args[0]:04x}"
        else:
            return f"{addr:04x}: {mnemonic} 0x{args[0]:02x}"
    else:
        return f"{addr:04x}: {mnemonic} {', '.join(f'0x{arg:02x}' for arg in args)}"

def analyze_bytecode(bytecode):
    instructions = disassemble(bytecode)
    
    # Find all jumps and their targets
    jumps = {}
    calls = {}
    
    for addr, mnemonic, args in instructions:
        if mnemonic in ["JMP", "JZ", "JNZ", "JEQ"] and args:
            jumps[addr] = args[0]
        elif mnemonic == "CALL" and args:
            calls[addr] = args[0]
    
    # Find potential subroutines (targets of CALL)
    subroutines = set(calls.values())
    
    # Find potential loops (backward jumps)
    loops = [(src, dst) for src, dst in jumps.items() if dst < src]
    
    return {
        "instructions": instructions,
        "jumps": jumps,
        "calls": calls,
        "subroutines": subroutines,
        "loops": loops
    }

def print_disassembly(bytecode, annotations=True):
    analysis = analyze_bytecode(bytecode)
    instructions = analysis["instructions"]
    subroutines = analysis["subroutines"]
    jump_targets = set(analysis["jumps"].values())
    
    for i, (addr, mnemonic, args) in enumerate(instructions):
        if annotations:
            if addr in subroutines:
                print(f"\nsub_{addr:04x}:")
            elif addr in jump_targets:
                print(f"\nloc_{addr:04x}:")
        
        print(format_instruction(addr, mnemonic, args))
        
        if annotations and mnemonic == "PUSH_IMM8" and args:
            val = args[0]
            if 32 <= val <= 126:
                print(f"      ; '{chr(val)}'")
            if val == 255:
                print(f"      ; RETURN_REG")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 disasm.py <bytecode.bin>")
        sys.exit(1)
    
    bytecode_path = pathlib.Path(sys.argv[1])
    if not bytecode_path.exists():
        print(f"Error: {bytecode_path} not found")
        sys.exit(1)
    
    bytecode = bytecode_path.read_bytes()
    print(f"Disassembly of {bytecode_path.name} ({len(bytecode)} bytes)")
    print("=" * 60)
    
    analysis = analyze_bytecode(bytecode)
    
    print(f"Instructions: {len(analysis['instructions'])}")
    print(f"Subroutines: {len(analysis['subroutines'])}")
    print(f"Loops: {len(analysis['loops'])}")
    
    if analysis['loops']:
        print("\nDetected loops:")
        for src, dst in analysis['loops']:
            print(f"  0x{src:04x} -> 0x{dst:04x}")
    
    print("\n" + "=" * 60 + "\n")
    
    print_disassembly(bytecode)

if __name__ == "__main__":
    main()