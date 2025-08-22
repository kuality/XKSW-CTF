from flask import Flask, request, render_template
from selenium import webdriver
from urllib.parse import parse_qs, quote

app = Flask(__name__)

try:
    FLAG = open("flag.txt", "r").read()
except:
    FLAG = "XKSW{flag_read_error}"

CONFIG = ['headless', 'window-size=1920x1080', 'disable-gpu', 'no-sandbox', 'disable-dev-shm-usage']

def BOT(xss):

    ChromeOptions = webdriver.ChromeOptions()

    for _ in CONFIG:
        ChromeOptions.add_argument(_)
    try:
        driver = webdriver.Chrome(options=ChromeOptions)
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)
        driver.get('http://xksw-ctf-web-nonce')

        driver.add_cookie({'name':'FLAG', 'value':FLAG.strip()})

        parse = parse_qs(xss)

        query = ''

        for key, value in parse.items():
            urlen = quote(value[0])
            query += f'{key}={urlen}&'
        print(query)
        driver.get(f'http://xksw-ctf-web-nonce/?{query}')

    except:
        driver.quit()
        return False

    driver.quit()
    return True

@app.route('/')
def send():
    if request.method == 'GET':
        xss = request.args.get('feedback', '')
        if xss:
            if BOT(xss):
                return render_template('index.html', feedback='피드백 전송 완료')
            else:
                return render_template('index.html', feedback='피드백 전송 에러')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

app.run('0.0.0.0', 8080)