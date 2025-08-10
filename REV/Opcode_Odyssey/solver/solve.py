import sys
from disasm import disassemble, opcodes

def extract_transformations(bytecode):
    instructions = disassemble(bytecode)
    
    # Find patterns where characters are read and transformed
    patterns = []
    i = 0
    
    while i < len(instructions):
        addr, mnem, args = instructions[i]
        
        # Look for READ instruction
        if mnem == "READ":
            # Track the transformations that follow
            transforms = []
            j = i + 1
            
            # Collect transformations until we hit a comparison
            while j < len(instructions):
                _, op, op_args = instructions[j]
                
                if op == "XOR" and j > i + 1:
                    # Check if this is the final XOR (comparison)
                    prev_op = instructions[j-1][1]
                    if prev_op == "PUSH_IMM8":
                        # This is likely the comparison value
                        expected_val = instructions[j-1][2][0]
                        transforms.append(("CMP", expected_val))
                        break
                
                if op in ["ADD", "SUB", "XOR", "AND", "OR", "ROL", "ROR", "MUL", "MOD"]:
                    # Get the operand from previous PUSH_IMM8
                    if j > 0 and instructions[j-1][1] == "PUSH_IMM8":
                        operand = instructions[j-1][2][0]
                        transforms.append((op, operand))
                    elif op in ["ROL", "ROR"] and j > 1 and instructions[j-2][1] == "PUSH_IMM8":
                        # For ROL/ROR, the count is pushed before SWAP
                        operand = instructions[j-2][2][0]
                        transforms.append((op, operand))
                
                j += 1
            
            if transforms:
                patterns.append(transforms)
        
        i += 1
    
    return patterns

# Reverse the transformations to get the original character
def reverse_transformations(expected_val, transforms):
    val = expected_val
    
    # Process transformations in reverse order
    for i in range(len(transforms) - 2, -1, -1):  # Skip the CMP at the end
        op, operand = transforms[i]
        
        if op == "XOR":
            val ^= operand
        elif op == "ADD":
            val = (val - operand) & 0xFF
        elif op == "SUB":
            val = (val + operand) & 0xFF
        elif op == "AND":
            # Can't reverse AND reliably
            pass
        elif op == "OR":
            # Can't reverse OR reliably
            pass
        elif op == "ROL":
            # Reverse ROL is ROR
            val = ((val >> operand) | (val << (8 - operand))) & 0xFF
        elif op == "ROR":
            # Reverse ROR is ROL
            val = ((val << operand) | (val >> (8 - operand))) & 0xFF
        elif op == "MUL":
            # Find multiplicative inverse (brute force for small numbers) -> faster than extended Euclidean algorithm for small values
            for x in range(256):
                if (x * operand) & 0xFF == val:
                    val = x
                    break
        elif op == "MOD":
            # Can't reverse MOD reliably
            pass
    
    return val

# Analyze the advanced bytecode with magic values
def analyze_advanced_bytecode(bytecode):
    instructions = disassemble(bytecode)
    
    # Find magic values stored in memory
    magic_values = []
    for i in range(len(instructions) - 2):
        if (instructions[i][1] == "PUSH_IMM8" and 
            instructions[i+1][1] == "PUSH_IMM8" and 
            instructions[i+2][1] == "STORE"):
            
            val = instructions[i][2][0]
            addr = instructions[i+1][2][0]
            if 0x80 <= addr <= 0x85:  # Magic value addresses
                magic_values.append(val)
    
    print(f"Found magic values: {[hex(v) for v in magic_values]}")
    
    # Extract character checks
    flag_chars = []
    char_idx = 0
    
    i = 0
    while i < len(instructions):
        if instructions[i][1] == "READ":
            # Find the expected value (look for final XOR before JZ)
            j = i + 1
            expected_val = None
            
            while j < len(instructions) - 1:
                if instructions[j][1] == "XOR" and instructions[j+1][1] == "JZ":
                    # The value before XOR is the expected transformed value
                    if instructions[j-1][1] == "PUSH_IMM8":
                        expected_val = instructions[j-1][2][0]
                        break
                j += 1
            
            if expected_val is not None:
                # Reverse the transformations
                # For the advanced bytecode:
                # 1. XOR with magic[i % 6]
                # 2. ADD (i*3 + 7)
                # 3. ROL by (i % 8)
                # 4. XOR 0x96
                # 5. ROR 2
                # 6. SUB ((i >> 2) + 0x11)
                
                val = expected_val
                
                # Reverse SUB ((i >> 2) + 0x11)
                val = (val + ((char_idx >> 2) + 0x11)) & 0xFF
                
                # Reverse ROR 2 (do ROL 2)
                val = ((val << 2) | (val >> 6)) & 0xFF
                
                # Reverse XOR 0x96
                val ^= 0x96
                
                # Reverse ROL by (i % 8) (do ROR)
                rot = char_idx % 8
                val = ((val >> rot) | (val << (8 - rot))) & 0xFF
                
                # Reverse ADD (i*3 + 7)
                val = (val - ((char_idx * 3) + 7)) & 0xFF
                
                # Reverse XOR with magic
                if magic_values:
                    magic_idx = char_idx % len(magic_values)
                    val ^= magic_values[magic_idx]
                
                if 32 <= val <= 126:
                    flag_chars.append(chr(val))
                else:
                    flag_chars.append(f"\\x{val:02x}")
                
                char_idx += 1
        
        i += 1
    
    return ''.join(flag_chars)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 solve.py <bytecode.bin>")
        sys.exit(1)
    
    with open(sys.argv[1], 'rb') as f:
        bytecode = f.read()
    
    print(f"Analyzing {sys.argv[1]} ({len(bytecode)} bytes)")
    print("=" * 60)
    
    # Try to extract the flag
    flag = analyze_advanced_bytecode(bytecode)
    
    print(f"\nRecovered flag: {flag}")
    
    # Also try simpler analysis
    patterns = extract_transformations(bytecode)
    if patterns:
        print(f"\nFound {len(patterns)} character checks")
        print("First few patterns:")
        for i, p in enumerate(patterns[:5]):
            print(f"  Char {i}: {p}")

if __name__ == "__main__":
    main()