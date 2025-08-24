#!/usr/bin/env python3
import sys, os, base64, tempfile, subprocess

PROB = os.path.abspath("./prob")

def main():
    sys.stdout.write("[+] Send BASE64 payload, end with a line: EOF\n> ")
    sys.stdout.flush()

    chunks = []
    total = 0
    limit = 128 * 1024 * 1024  # 128MB safety

    while True:
        buf = sys.stdin.buffer.readline(1024)
        if not buf:
            break

        if buf.strip() == b"EOF":
            break
        chunks.append(buf)
        total += len(buf)
        if total > limit:
            print("[-] input too large"); return 1

    if not chunks:
        print("[-] no input"); return 1

    b64_bytes = b"".join(chunks)

    try:
        blob = base64.b64decode(b64_bytes, validate=False)
    except Exception as e:
        print("[-] decode error:", e); return 1

    with tempfile.TemporaryDirectory() as workdir:
        path = os.path.join(workdir, "payload")
        with open(path, "wb") as f:
            f.write(blob)

        if not (os.path.exists(PROB) and os.access(PROB, os.X_OK)):
            print("[-] ./prob not found or not executable")
            return 1

        return subprocess.call([PROB, path])

if __name__ == "__main__":
    raise SystemExit(main())
