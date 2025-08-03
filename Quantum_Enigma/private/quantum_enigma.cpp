#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <sstream>

using namespace std;

class QuantumSimulator {
private:
    unsigned char rotateLeft(unsigned char val, int shift) {
        shift = shift % 8;
        return ((val << shift) | (val >> (8 - shift))) & 0xFF;
    }
    
    unsigned char rotateRight(unsigned char val, int shift) {
        shift = shift % 8;
        return ((val >> shift) | (val << (8 - shift))) & 0xFF;
    }
    
    unsigned char reversibleTransform(unsigned char val, int key) {
        val ^= key;
        val = rotateLeft(val, 3);
        val ^= (key * 3 + 17);
        return val;
    }
    
    unsigned char controlledNot(unsigned char val, int control, int target) {
        if (val & (1 << control)) {
            val ^= (1 << target);
        }
        return val;
    }

public:
    string processFlag(const string& input) {
        string result;
        
        for (size_t i = 0; i < input.length(); i++) {
            unsigned char c = input[i];
            
            // Layer 1: Position-based rotation
            c = rotateLeft(c, (i % 7) + 1);
            
            // Layer 2: XOR with position-based key
            c ^= (i * 23 + 11) & 0xFF;
            
            // Layer 3: Reversible transform
            c = reversibleTransform(c, (i * 17 + 5) & 0xFF);
            
            // Layer 4: CNOT gates
            c = controlledNot(c, 7, 0);
            c = controlledNot(c, 6, 1);
            c = controlledNot(c, 5, 2);
            c = controlledNot(c, 4, 3);
            
            // Layer 5: Another rotation
            c = rotateRight(c, (i % 5) + 1);
            
            // Layer 6: XOR with magic number
            c ^= 0x5A;
            
            // Layer 7: Final position-based XOR
            c ^= ((i * i + 31) % 256);
            
            result += c;
        }
        
        return result;
    }
};

string bytesToHex(const string& bytes) {
    stringstream ss;
    for (unsigned char c : bytes) {
        ss << hex << setw(2) << setfill('0') << (int)c;
    }
    return ss.str();
}

int main() {
    cout << "=== Quantum Enigma ===" << endl;
    cout << "Enter the flag: ";
    
    string input;
    getline(cin, input);
    
    QuantumSimulator qs;
    string processed = qs.processFlag(input);
    string hexOutput = bytesToHex(processed);
    
    // Expected output will be calculated
    const string expected = "2ade8dc77a98c58de910f35cb27ee352af3cee942751baa80dceeb48ca078bccfdbde717cabad4520192efcf69514c2c75ccad2203091fa75880f87376b93b9391803298a49a";
    
    if (hexOutput == expected) {
        cout << "Quantum simulation successful! The flag is correct." << endl;
    } else {
        cout << "Quantum state mismatch. Invalid flag." << endl;
        cout << "Your output: " << hexOutput << endl;
    }
    
    return 0;
}