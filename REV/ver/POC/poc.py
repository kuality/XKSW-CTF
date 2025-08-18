def recover_original(paradoxified: str) -> str:
    n = len(paradoxified)
    half = n // 2
    s = [''] * n
    for i in range(half):
        s[i] = paradoxified[2 * i]              # 짝수 인덱스 -> 앞 절반
        if 2 * i + 1 < n:
            s[half + i] = paradoxified[2 * i + 1]  # 홀수 인덱스 -> 뒤 절반
    if n % 2 == 1:  # 길이가 홀수면 마지막 글자는 그대로
        s[-1] = paradoxified[-1]
    return ''.join(s)

target = "cVjrBMrFd9WysMwGXt31IawzaA3="
orig = recover_original(target)
print("Recovered input:", orig)

# base64 디코딩
import base64, binascii
try:
    print("flag:", base64.b64decode(orig).decode())
except (binascii.Error, UnicodeDecodeError):
    pass

