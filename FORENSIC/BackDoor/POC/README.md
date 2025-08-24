# Write-up

문제 파일을 다운받으면 Image2.E01 이미지 파일 하나를 얻을 수 있다.
이 파일을 ftk imager로 열어 확인해보면 pc의 구조를 확인할 수 있다.
Basic data partition에서 C:\Users 경로로 이동하면 여러 사용자를 확인할 수 있다.

사용자는 아래와 같다.
- ADMIN
- GUEST1
- GUEST2
- GUEST3
- MAIN
- TEST

우선 침입 정황이 있다고 하니, C:\Windows\System32\winevt\Logs\Security.evtx 경로로 이동하여 원격 접속 기록을 확인해보면 아래와 같이 4624(로그인 성공), Type 10(원격 RDP)를 확인할 수 있고
이후 내용을 확인해보면 GUEST3에 접속한 것을 확인할 수 있다.
* 추가 힌트로는 C:\Users\GUEST2\Pictures에 보면 제목 없음.jpg에 I love 3!!!라는 것으로 GUEST3가 공격 당했음을 간접적으로 나타낸다.
<img width="1994" height="1350" alt="image" src="https://github.com/user-attachments/assets/f86b3627-1376-48da-914b-4da0f291c1f3" />

원격 접속 기록을 통해 GUEST3가 공격 당했음은 확인했으니 해당 시간대의 파일 생성 흔적을 $MFT 등으로 확인하고, 생성한 파일이 실제 실행된 건지 Prefetch를 통해 확인한 후 파일이 생성된 경로인 C:\Users\GUEST3\OneDrive를 확인해보면 onenoteup.exe라는 의심되는 파일이 찾을 수 있고 이 exe파일을 IDA, Ghidra 등을 통해 리버싱하거나 pyinstaller로 생성되었다는 것을 파일 분석으로 확인하면 pyinstxtractor등으로 pyc파일을 추출한 뒤(reverse.pyc) pycdc나 uncompyle6 등의 python 디컴파일 도구를 통해 py파일로 만들어 내용을 확인하면 flag가 담긴 코드를 확인할 수 있다.
<img width="1974" height="1096" alt="스크린샷 2025-08-24 114006" src="https://github.com/user-attachments/assets/4803be6c-f730-4854-9676-d01d4439faad" />
<img width="1823" height="941" alt="스크린샷 2025-08-24 114229" src="https://github.com/user-attachments/assets/81dde924-ec92-40ff-aaf4-c0e82650555b" />
<img width="1897" height="670" alt="스크린샷 2025-08-24 114318" src="https://github.com/user-attachments/assets/e6a5b328-851c-4b3a-bf05-6e2fea11c777" />
<img width="1943" height="490" alt="스크린샷 2025-08-24 114330" src="https://github.com/user-attachments/assets/31a4205e-7144-459d-895b-1c0d86a4f39e" />

** 현재 python버전이 낮춰서 진행하였고, powershell 기록도 남겨두었습니다.(사진 첨부)
<img width="2280" height="1106" alt="스크린샷 2025-08-24 113650" src="https://github.com/user-attachments/assets/f560a448-11d5-4ea8-b41a-ae5416627839" />
