# XKSW-CTF
Title
-----------
Note

Author
-----------
r0jin

Description
-----------
흔한 Note 문제에요

Level
-----------
High

Write-up
-----------
management_chunks 데이터 free 후 해당 값을 NULL로 지우지 않기 때문에 msg_msg 구조체 할당 후 Kernel Address Leak 및 modprobe Overwrite를 통해 Exploit이 가능하다. 
단, Heap Spray를 사용해서 Exploit의 안정성을 높여주거나, 여러번의 Exploit 실행을 통해 권한 상승을 수행하여야 한다. 첨부된 PoC에서는 후자의 방식으로 권한 상승을 수행하였다.