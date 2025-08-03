#!/usr/bin/env python3

class QuantumEnigmaSolver:
    def __init__(self):
        self.expected_hex = "2ade8dc77a98c58de910f35cb27ee352af3cee942751baa80dceeb48ca078bccfdbde717cabad4520192efcf69514c2c75ccad2203091fa75880f87376b93b9391803298a49a"
    
    def rotate_left(self, val, shift):
        """Rotate bits left"""
        shift = shift % 8
        return ((val << shift) | (val >> (8 - shift))) & 0xFF
    
    def rotate_right(self, val, shift):
        """Rotate bits right"""
        shift = shift % 8
        return ((val >> shift) | (val << (8 - shift))) & 0xFF
    
    def reversible_transform(self, val, key):
        """Apply reversible transformation"""
        val ^= key
        val = self.rotate_left(val, 3)
        val ^= (key * 3 + 17) & 0xFF
        return val
    
    def reversible_transform_inv(self, val, key):
        """Inverse of reversible transformation"""
        val ^= (key * 3 + 17) & 0xFF
        val = self.rotate_right(val, 3)
        val ^= key
        return val
    
    def controlled_not(self, val, control, target):
        """CNOT gate (self-inverse)"""
        if val & (1 << control):
            val ^= (1 << target)
        return val
    
    def decrypt(self):
        """Decrypt the flag from the expected output"""
        # Convert hex to bytes
        encrypted = bytes.fromhex(self.expected_hex)
        result = []
        
        for i in range(len(encrypted)):
            c = encrypted[i]
            
            # Reverse Layer 7: Final position-based XOR
            c ^= ((i * i + 31) % 256)
            
            # Reverse Layer 6: XOR with magic number
            c ^= 0x5A
            
            # Reverse Layer 5: Another rotation (right becomes left)
            c = self.rotate_left(c, (i % 5) + 1)
            
            # Reverse Layer 4: CNOT gates (self-inverse, apply in same order)
            c = self.controlled_not(c, 4, 3)
            c = self.controlled_not(c, 5, 2)
            c = self.controlled_not(c, 6, 1)
            c = self.controlled_not(c, 7, 0)
            
            # Reverse Layer 3: Reversible transform
            c = self.reversible_transform_inv(c, (i * 17 + 5) & 0xFF)
            
            # Reverse Layer 2: XOR with position-based key
            c ^= (i * 23 + 11) & 0xFF
            
            # Reverse Layer 1: Position-based rotation (left becomes right)
            c = self.rotate_right(c, (i % 7) + 1)
            
            result.append(chr(c))
        
        return ''.join(result)
    
    def encrypt(self, flag):
        """Encrypt the flag to verify our solution"""
        result = []
        
        for i in range(len(flag)):
            c = ord(flag[i])
            
            # Layer 1: Position-based rotation
            c = self.rotate_left(c, (i % 7) + 1)
            
            # Layer 2: XOR with position-based key
            c ^= (i * 23 + 11) & 0xFF
            
            # Layer 3: Reversible transform
            c = self.reversible_transform(c, (i * 17 + 5) & 0xFF)
            
            # Layer 4: CNOT gates
            c = self.controlled_not(c, 7, 0)
            c = self.controlled_not(c, 6, 1)
            c = self.controlled_not(c, 5, 2)
            c = self.controlled_not(c, 4, 3)
            
            # Layer 5: Another rotation
            c = self.rotate_right(c, (i % 5) + 1)
            
            # Layer 6: XOR with magic number
            c ^= 0x5A
            
            # Layer 7: Final position-based XOR
            c ^= ((i * i + 31) % 256)
            
            result.append(c)
        
        return ''.join(f'{b:02x}' for b in result)


def main():
    solver = QuantumEnigmaSolver()
    
    print("Quantum Enigma Solver")
    print("=" * 50)
    print(f"Expected output: {solver.expected_hex}")
    
    # Decrypt the flag
    flag = solver.decrypt()
    print(f"\nDecrypted flag: {flag}")
    
    # Verify by re-encrypting
    encrypted = solver.encrypt(flag)
    if encrypted == solver.expected_hex:
        print("\nVerification: SUCCESS!")
        print("The decryption is correct.")
    else:
        print("\nVerification: FAILED")
        print(f"Re-encrypted: {encrypted}")
    
    return flag


if __name__ == "__main__":
    main()