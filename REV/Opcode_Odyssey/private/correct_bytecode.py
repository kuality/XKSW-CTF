# VM Opcodes
HALT = 0x00
PUSH_IMM8 = 0x01
PUSH_IMM16 = 0x02
POP = 0x03
DUP = 0x04
SWAP = 0x05

ADD = 0x10
SUB = 0x11
MUL = 0x12
MOD = 0x13
XOR = 0x14
AND = 0x15
OR = 0x16
NOT = 0x17
ROL = 0x18
ROR = 0x19

LOAD = 0x20
STORE = 0x21
LOAD_IND = 0x22

JMP = 0x30
JZ = 0x31
JNZ = 0x32
JEQ = 0x33

READ = 0x40
WRITE = 0x41

CALL = 0x50
RET = 0x51

RETURN_REG = 255

# Create correct bytecode
def create_correct_bytecode():
    flag = "XKSW{3934a679f792817b6404eec91d1cb757d6724f389f286fa0d70a78366bf60e5f}"
    bytecode = bytearray()
    
    # Initialize return register to 0 (success)
    bytecode.extend([
        PUSH_IMM8, 0,
        PUSH_IMM8, RETURN_REG,
        STORE
    ])
    
    # For each character
    for i, c in enumerate(flag):
        # Read character
        bytecode.extend([READ])
        
        # Transform: (char + 0x13) ^ (i * 7) ROL 3 ^ 0xA5
        bytecode.extend([
            PUSH_IMM8, 0x13,
            ADD,
            PUSH_IMM8, (i * 7) & 0xFF,
            XOR,
            PUSH_IMM8, 3,
            SWAP,
            ROL,
            PUSH_IMM8, 0xA5,
            XOR
        ])
        
        # Calculate expected value
        val = ord(c)
        val = (val + 0x13) & 0xFF
        val = ((val ^ (i * 7)) & 0xFF)
        val = ((val << 3) | (val >> 5)) & 0xFF
        val = (val ^ 0xA5) & 0xFF
        
        # Compare
        bytecode.extend([
            PUSH_IMM8, val,
            XOR  # Result is 0 if match
        ])
        
        # JZ with embedded address
        skip_addr = len(bytecode) + 3 + 5  # Skip JZ itself and error handling (5 bytes)
        bytecode.extend([
            JZ, skip_addr & 0xFF, (skip_addr >> 8) & 0xFF
        ])
        
        # Mismatch - set error
        bytecode.extend([
            PUSH_IMM8, 1,
            PUSH_IMM8, RETURN_REG,
            STORE
        ])
    
    # Success - all checks passed
    bytecode.extend([HALT])
    
    return bytes(bytecode)

def create_test_bytecode():
    """Create test bytecode that checks for 'X'"""
    bytecode = bytearray()
    
    # Init return to 0
    bytecode.extend([
        PUSH_IMM8, 0,
        PUSH_IMM8, RETURN_REG,
        STORE
    ])
    
    # Read and check 'X'
    bytecode.extend([
        READ,
        PUSH_IMM8, ord('X'),
        XOR
    ])
    
    # JZ to success
    # Current position is 9, JZ takes 3 bytes, error handling takes 6 bytes
    # So HALT will be at position 9 + 3 + 6 = 18
    # But actually, let's calculate it properly
    # Error handling: PUSH_IMM8(2) + PUSH_IMM8(2) + STORE(1) = 5 bytes, not 6
    success_addr = len(bytecode) + 3 + 5
    bytecode.extend([
        JZ, success_addr & 0xFF, (success_addr >> 8) & 0xFF
    ])
    
    # Error
    bytecode.extend([
        PUSH_IMM8, 1,
        PUSH_IMM8, RETURN_REG,
        STORE
    ])
    
    # Success
    bytecode.extend([HALT])
    
    return bytes(bytecode)

# Create more complex bytecode with additional operations
def create_advanced_bytecode():
    flag = "XKSW{3934a679f792817b6404eec91d1cb757d6724f389f286fa0d70a78366bf60e5f}"
    bytecode = bytearray()
    
    # Initialize
    bytecode.extend([
        PUSH_IMM8, 0,
        PUSH_IMM8, RETURN_REG,
        STORE
    ])
    
    # Store magic constants in memory for obfuscation
    MAGIC_BASE = 0x80
    magic_values = [0x42, 0x13, 0x37, 0x99, 0xAA, 0x55]
    for i, val in enumerate(magic_values):
        bytecode.extend([
            PUSH_IMM8, val,
            PUSH_IMM8, MAGIC_BASE + i,
            STORE
        ])
    
    # Check each character with complex transformations
    for i, c in enumerate(flag):
        # Read character
        bytecode.extend([READ])
        
        # Load magic value based on position
        magic_idx = i % len(magic_values)
        bytecode.extend([
            PUSH_IMM8, MAGIC_BASE + magic_idx,
            LOAD,
            XOR  # XOR with magic
        ])
        
        # More transformations
        bytecode.extend([
            PUSH_IMM8, ((i * 3) + 7) & 0xFF,
            ADD,
            PUSH_IMM8, (i % 8),
            SWAP,
            ROL,  # Rotate by position
            PUSH_IMM8, 0x96,
            XOR,
            PUSH_IMM8, 2,
            SWAP,
            ROR,  # Rotate right by 2
            PUSH_IMM8, ((i >> 2) + 0x11) & 0xFF,
            SUB
        ])
        
        # Calculate expected value
        val = ord(c)
        val ^= magic_values[magic_idx]
        val = (val + ((i * 3) + 7)) & 0xFF
        val = ((val << (i % 8)) | (val >> (8 - (i % 8)))) & 0xFF
        val ^= 0x96
        val = ((val >> 2) | (val << 6)) & 0xFF
        val = (val - ((i >> 2) + 0x11)) & 0xFF
        
        # Compare
        bytecode.extend([
            PUSH_IMM8, val,
            XOR
        ])
        
        # Jump if match
        skip_addr = len(bytecode) + 3 + 5  # JZ (3) + error handling (5)
        bytecode.extend([
            JZ, skip_addr & 0xFF, (skip_addr >> 8) & 0xFF
        ])
        
        # Error
        bytecode.extend([
            PUSH_IMM8, 1,
            PUSH_IMM8, RETURN_REG,
            STORE
        ])
    
    bytecode.extend([HALT])
    
    return bytes(bytecode)

if __name__ == "__main__":
    # Test bytecode
    test_bc = create_test_bytecode()
    with open("test_correct.bin", "wb") as f:
        f.write(test_bc)
    print(f"Test bytecode: {len(test_bc)} bytes")
    
    # flag check 1
    simple_bc = create_correct_bytecode()
    with open("simple_flag.bin", "wb") as f:
        f.write(simple_bc)
    print(f"Simple flag bytecode: {len(simple_bc)} bytes")
    
    # flag check 2
    advanced_bc = create_advanced_bytecode()
    with open("../public/ancient_scroll.bin", "wb") as f:
        f.write(advanced_bc)
    print(f"Advanced flag bytecode: {len(advanced_bc)} bytes")