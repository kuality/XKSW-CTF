#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <seccomp.h>
#include <sys/mman.h>
#include <linux/seccomp.h>

void init_buf() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
}

void sandbox() {
    scmp_filter_ctx ctx;
	ctx = seccomp_init(SCMP_ACT_KILL);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(sendfile), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mmap), 0);
	seccomp_load(ctx);
}

int main() {
    init_buf();
    int fd = open("./flag", O_RDONLY);
    char *shellcode_addr = (char *)mmap(0xdead0000, 0x1000, 7, 34, -1, 0);
    read(0, shellcode_addr, 0x1000);
    sandbox();
    ((void(*)())shellcode_addr)();
}