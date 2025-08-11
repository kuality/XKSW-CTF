// mips-linux-gnu-gcc -Wl,-z,noexecstack -fno-stack-protector   -o prob prob.c -static
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>


void * stack_addr;

void initialize(){
        setvbuf(stdin, NULL, _IONBF, 0);
        setvbuf(stdout, NULL, _IONBF, 0);
        setvbuf(stderr, NULL, _IONBF, 0);
}

void gadget(){
	asm("addiu  $sp, $sp, 0x10");
	asm("lw    $t9, 0x24($sp)");
	asm("lw      $a2, 0x20($sp)");
	asm("lw      $a1, 0x1C($sp)");
	asm("lw      $a0, 0x18($sp)");
	asm("jr      $t9");
}

int main(){
	initialize();
	char buf[0x100];

	stack_addr = ((uintptr_t)&buf[0]) & ~((uintptr_t)0x1000 - 1);
	printf("Buf : %p\n", &buf);
	memset(buf, 0, 0x100);

	read(0, buf, 0x200);
	if (mprotect(stack_addr, 0x1000, 6) != 0) {
                exit(1);
		return 1;
        }

	return 0;
}
