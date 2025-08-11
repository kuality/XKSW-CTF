# make_target.py
def make_target(flag: str) -> str:
    n = len(flag)
    half = n // 2
    t = []
    for i in range(half):
        t.append(flag[i])          # 짝수 인덱스
        t.append(flag[half + i])   # 홀수 인덱스
    if n % 2 == 1:
        t.append(flag[-1])         # 길이가 홀수면 마지막 문자
    return "".join(t)

if __name__ == "__main__":
    real_flag = "cjBrdWswX3Iwa3VrMF9yMGt1azA="   # 타겟
    print(make_target(real_flag))