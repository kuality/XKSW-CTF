#include <stdio.h>
#include <string.h>

const char* target = "cVjrBMrFd9WysMwGXt31IawzaA3="; // make_target.py결과값

int main() {
    char s[256];
    char v8[256] = { 0 };
    printf("What do you think the flag is? ");
    fflush(stdout);

    fgets(s, 256, stdin);
    size_t len = strcspn(s, "\n");
    s[len] = '\0';

    if (strlen(target) == len) {
        size_t half_len = len >> 1;
        for (size_t i = 0; i < half_len; i++) {
            v8[2 * i] = s[i];
            v8[2 * i + 1] = s[half_len + i];
        }

        // 마지막 글자 처리 (길이가 홀수일 경우)
        if (len % 2 == 1) {
            v8[len - 1] = s[len - 1];
        }

        v8[len] = '\0';

        if (strcmp(target, v8) == 0) {
            puts("That's right! Now decode it and submit the flag :D");
            return 0;
        }
        else {
            puts("You got the flag wrong >:(");
            return 1;
        }
    }
    else {
        puts("Bad length >:(");
        return 1;
    }
}
