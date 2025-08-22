from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import parse_qs, quote
import os

app = Flask(__name__)

try:
    FLAG = open("flag.txt", "r").read()
except:
    FLAG = "XKSW{flag_read_error}"

CONFIG = [
    '--headless',
    '--window-size=1920x1080',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-web-security',
    '--disable-features=VizDisplayCompositor',
    '--disable-extensions',
    '--disable-plugins',
    '--disable-images',
    '--disable-javascript-harmony-shipping',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    '--disable-features=TranslateUI',
    '--disable-ipc-flooding-protection'
]

def BOT(xss):
    driver = None
    try:
        ChromeOptions = webdriver.ChromeOptions()
        
        # ARM64 아키텍처 호환성을 위한 설정
        ChromeOptions.binary_location = os.environ.get('CHROME_BIN', '/usr/bin/chromium')
        
        for arg in CONFIG:
            ChromeOptions.add_argument(arg)
        
        # ChromeDriver 서비스 설정
        service = Service(executable_path=os.environ.get('CHROMEDRIVER_PATH', '/usr/bin/chromedriver'))
        
        driver = webdriver.Chrome(service=service, options=ChromeOptions)
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

    except Exception as e:
        print(f"Error in BOT function: {e}")
        if driver:
            try:
                driver.quit()
            except:
                pass
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

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