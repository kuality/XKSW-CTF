#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define STACK_SIZE  512
#define MEM_SIZE    1024
#define CODE_MAX    10000

// Stack-based VM with enhanced operations
static uint32_t stack[STACK_SIZE];
static int sp = 0;  // Stack pointer
static uint8_t mem[MEM_SIZE];
static uint8_t code[CODE_MAX];
static int pc = 0, clen = 0;

// Return value stored in mem[255] instead of typical stack top
#define RETURN_REG 255

static inline uint8_t fetch(void)
{
    if (pc >= clen) { 
        fputs("Journey beyond the scroll boundaries\n", stderr); 
        exit(1); 
    }
    return code[pc++];
}

static inline uint16_t fetch16(void)
{
    uint16_t val = fetch();
    val |= (uint16_t)fetch() << 8;
    return val;
}

static inline void push(uint32_t val)
{
    if (sp >= STACK_SIZE) {
        fputs("The stack runneth over - too many secrets\n", stderr);
        exit(1);
    }
    stack[sp++] = val;
}

static inline uint32_t pop(void)
{
    if (sp <= 0) {
        fputs("The stack is empty - no secrets remain\n", stderr);
        exit(1);
    }
    return stack[--sp];
}

static uint8_t run_vm(void)
{
    for (;;) {
        uint8_t op = fetch();
        
        switch (op) {
        case 0x00: // HALT
            return mem[RETURN_REG];
            
        case 0x01: { // PUSH_IMM8
            uint8_t val = fetch();
            push(val);
            break;
        }
        
        case 0x02: { // PUSH_IMM16
            uint16_t val = fetch16();
            push(val);
            break;
        }
        
        case 0x03: { // POP (discard top)
            pop();
            break;
        }
        
        case 0x04: { // DUP
            if (sp <= 0) {
                fputs("The stack is empty - no secrets remain\n", stderr);
                exit(1);
            }
            push(stack[sp-1]);
            break;
        }
        
        case 0x05: { // SWAP
            if (sp < 2) {
                fputs("The stack is empty - no secrets remain\n", stderr);
                exit(1);
            }
            uint32_t tmp = stack[sp-1];
            stack[sp-1] = stack[sp-2];
            stack[sp-2] = tmp;
            break;
        }
        
        case 0x10: { // ADD
            uint32_t b = pop();
            uint32_t a = pop();
            push((a + b) & 0xFF);
            break;
        }
        
        case 0x11: { // SUB
            uint32_t b = pop();
            uint32_t a = pop();
            push((a - b) & 0xFF);
            break;
        }
        
        case 0x12: { // MUL
            uint32_t b = pop();
            uint32_t a = pop();
            push((a * b) & 0xFF);
            break;
        }
        
        case 0x13: { // MOD
            uint32_t b = pop();
            uint32_t a = pop();
            if (b == 0) {
                fputs("Cannot divide by the void\n", stderr);
                exit(1);
            }
            push(a % b);
            break;
        }
        
        case 0x14: { // XOR
            uint32_t b = pop();
            uint32_t a = pop();
            push(a ^ b);
            break;
        }
        
        case 0x15: { // AND
            uint32_t b = pop();
            uint32_t a = pop();
            push(a & b);
            break;
        }
        
        case 0x16: { // OR
            uint32_t b = pop();
            uint32_t a = pop();
            push(a | b);
            break;
        }
        
        case 0x17: { // NOT
            uint32_t a = pop();
            push(~a & 0xFF);
            break;
        }
        
        case 0x18: { // ROL (rotate left)
            uint32_t val = pop();
            uint32_t count = pop() & 7;
            push(((val << count) | (val >> (8 - count))) & 0xFF);
            break;
        }
        
        case 0x19: { // ROR (rotate right)
            uint32_t val = pop();
            uint32_t count = pop() & 7;
            push(((val >> count) | (val << (8 - count))) & 0xFF);
            break;
        }
        
        case 0x20: { // LOAD (from memory)
            uint32_t addr = pop();
            if (addr >= MEM_SIZE) {
                fputs("Memory access forbidden - beyond the sacred bounds\n", stderr);
                exit(1);
            }
            push(mem[addr]);
            break;
        }
        
        case 0x21: { // STORE (to memory)
            uint32_t addr = pop();
            uint32_t val = pop();
            if (addr >= MEM_SIZE) {
                fputs("Memory access forbidden - beyond the sacred bounds\n", stderr);
                exit(1);
            }
            mem[addr] = val & 0xFF;
            break;
        }
        
        case 0x22: { // LOAD_IND (indirect load)
            uint32_t addr_ptr = pop();
            if (addr_ptr >= MEM_SIZE) {
                fputs("Memory access forbidden - beyond the sacred bounds\n", stderr);
                exit(1);
            }
            uint32_t addr = mem[addr_ptr];
            if (addr >= MEM_SIZE) {
                fputs("Memory access forbidden - beyond the sacred bounds\n", stderr);
                exit(1);
            }
            push(mem[addr]);
            break;
        }
        
        case 0x30: { // JMP
            uint16_t addr = fetch16();
            pc = addr;
            break;
        }
        
        case 0x31: { // JZ (jump if zero)
            uint16_t addr = fetch16();
            uint32_t val = pop();
            if (val == 0) {
                pc = addr;
            }
            break;
        }
        
        case 0x32: { // JNZ (jump if not zero)
            uint16_t addr = fetch16();
            uint32_t val = pop();
            if (val != 0) {
                pc = addr;
            }
            break;
        }
        
        case 0x33: { // JEQ (jump if equal)
            uint16_t addr = fetch16();
            uint32_t b = pop();
            uint32_t a = pop();
            if (a == b) {
                pc = addr;
            }
            break;
        }
        
        case 0x40: { // READ (input byte)
            int c = getchar();
            push(c & 0xFF);
            break;
        }
        
        case 0x41: { // WRITE (output byte)
            uint32_t val = pop();
            putchar(val & 0xFF);
            break;
        }
        
        case 0x50: { // CALL (push return address)
            uint16_t addr = fetch16();
            push(pc);
            pc = addr;
            break;
        }
        
        case 0x51: { // RET (pop return address)
            pc = pop();
            break;
        }
        
        default:
            fprintf(stderr, "Forbidden opcode 0x%02x encountered at scroll position %d\n", op, pc - 1);
            exit(1);
        }
    }
}

static void load_code(const char *path)
{
    FILE *fp = fopen(path, "rb");
    if (!fp) { 
        perror("fopen"); 
        exit(1); 
    }
    
    clen = fread(code, 1, CODE_MAX, fp);
    fclose(fp);
    
    if (clen <= 0) { 
        fputs("The ancient scroll is empty\n", stderr); 
        exit(1); 
    }
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        puts("Usage: ./prob <path-to-ancient-scroll>");
        return 1;
    }
    
    printf("=== Opcode Odyssey ===\n");
    printf("Enter the sacred bytecode sequence: ");
    fflush(stdout);
    
    load_code(argv[1]);
    
    if (run_vm() == 0) {
        puts("\n[+] Journey complete. You have mastered the ancient opcodes!");
    } else {
        puts("\n[-] Journey failed. The opcodes reject your sequence.");
    }
    
    return 0;
}