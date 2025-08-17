# XKSW-CTF
Title
-----------
mips_pwn

Author
-----------
r0jin

Description
-----------
easy mips

Level
-----------
low

Write-up
-----------
bof 취약점이 발생한다. mips ROP를 통해 mprotect 함수를 호출하여 메모리에 rwx 권한을 부여한 뒤 shellcode를 사용하여 풀이가 가능하다.