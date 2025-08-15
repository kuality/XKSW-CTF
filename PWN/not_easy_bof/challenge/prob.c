#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
    init();
    srand(time(NULL));
    char buf[128];
    while(1) {
        printf("> ");
        read(0, buf, 0x100);
        if (strncmp(buf, "exit", 4) == 0) {
            break;
        }
        int key = rand() & 0xFF;
        for(int i = 0; i < strlen(buf); i++) {
            printf("%c", buf[i] ^ key);
        }
    }
}