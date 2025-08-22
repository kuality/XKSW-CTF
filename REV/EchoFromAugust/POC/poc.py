def xor_decode(buf: bytes, key: int = 0x55) -> bytes:
    return bytes(b ^ key for b in buf)

def c_string(b: bytes) -> bytes:
    try:
        end = b.index(0)
        return b[:end]
    except ValueError:
        return b

def main():
    encoded_ip = bytes([
        0x64, 0x6C, 0x67, 0x7B, 0x64, 0x63, 0x6D, 0x7B,
        0x64, 0x65, 0x65, 0x7B, 0x62, 0x62, 0x55
    ])

    decoded = xor_decode(encoded_ip)     
    ip_bytes = c_string(decoded)             
    ip = ip_bytes.decode('ascii')             

    port = 7777         

    print(f"IP: {ip}")
    print(f"Port: {port}")

if __name__ == "__main__":
    main()
