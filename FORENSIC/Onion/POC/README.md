# Write-up

문제 파일을 다운받으면 Image1.E01 이미지 파일 하나를 얻을 수 있다.
이 파일을 ftk imager로 열어 확인해보면 pc의 구조를 확인할 수 있다.
Basic data partition에서 C:\Users\Kimyeonhap 경로로 이동하면 사용자의 여러 폴더를 확인할 수 있다.

우선 Downloads 폴더를 확인하면 설치된 프로그램을 확인할 수 있는데
- autopsy
- notepad3
- npp.8.8.4
- sublimetxt
- VSCode
등을 설치했음을 확인할 수 있다.

우선 문제에서 언급되었다싶이 메모장과 유사한 도구로 위장한 것 같다 라는 내용이 있고 실제 notepad3를 다운받으면
'Notepad3_6.25.714.1_x64_Setup.exe'와 같은 이름으로 다운되기 때문에 notepad3.exe 파일이 위장된 파일임을 의심할 수 있다.
또한, Documents폴더에 가보면 Tor Browser가 설치되어 있는 것을 확인할 수 있다.
notepad3.exe는 Tor Browser 설치 파일인 것이고 이를 위장한 것을 알 수 있다.
실제 접속 주소를 찾아야 하는 문제이니 어떤 주소를 접했는지 확인하기 위해 places.sqlite를 분석하면 된다.
C:\User\Kimyeonhap\Documents\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default 경로에 places.sqlite가 존재한다.
이 파일을 DB Browser(SQLite)와 같은 db sqlite분석 프로그램으로 열어보면 된다.
Tor Browser 특성상 방문한 기록은 저장되어 있지 않으니 저장되는 기록인 북마크해둔 주소를 moz_bookmarks 확인해보면 Tor Onion이라는 기본적으로 북마크 되어 있지 않은 이름이 있다.
주소를 확인하기 위해 moz_places 정보와 합쳐서 결과를 확인하기 위해 아래와 같은 sql를 실행해준다.

```
SELECT moz_places.url, moz_bookmarks.title
FROM moz_bookmarks
JOIN moz_places ON moz_bookmarks.fk = moz_places.id
WHERE moz_places.url LIKE '%.onion%';
```
그러면 아래와 같이 flag값인 onion주소를 확인할 수 있다.
<img width="2880" height="1516" alt="풀이" src="https://github.com/user-attachments/assets/36886e55-7f42-4ef8-bb08-46c2db715f8e" />

* 참고로 이 주소값의 소문자를 대문자로 바꾸어 base32에 넣으면 아래와 같은 내용이 들어있다.
-> ThankUforsolvingtheUnionCTFproblem.


