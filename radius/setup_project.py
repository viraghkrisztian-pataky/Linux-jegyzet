# setup_project.py
import os

print("[*] RADIUS projekt generálása (Natív, könyvtárfüggetlen jelszókezeléssel)...")

server_code = """import socket
import os
import datetime
import hashlib

def clean_strict(s):
    if not s:
        return ""
    return s.replace('\\\\r', '').replace('\\\\n', '').replace('\\\\x00', '').replace('\\x00', '').strip()

def load_devices():
    devices = {}
    if not os.path.exists("devices.txt"):
        return {}
    
    with open("devices.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(";")
            if len(parts) >= 2:
                ip = clean_strict(parts[0])
                secret = clean_strict(parts[1])
                hostname = clean_strict(parts[2]) if len(parts) > 2 else "Unknown"
                devices[ip] = {"secret": secret.encode('utf-8'), "hostname": hostname}
    return devices

def load_users():
    users = {}
    if not os.path.exists("users.txt"):
        return {}
            
    with open("users.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(";")
            if len(parts) == 2:
                username = clean_strict(parts[0])
                password = clean_strict(parts[1])
                users[username] = password
    return users

def log_event(ip, username, status):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{now};{ip};{username};{status}\\n")

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(("0.0.0.0", 1812))
        print("==================================================")
        print("   KERESZTPLATFORMOS NATÍV RADIUS SZERVER         ")
        print("==================================================")
        print("[+] Szerver sikeresen elindult az UDP 1812-es porton.")
        print("[*] Figyelés minden hálózati interfészen (0.0.0.0)...\\n")
    except Exception as e:
        print(f"[-] Hiba a porthoz rendelés során: {e}")
        return

    while True:
        try:
            data, addr = sock.recvfrom(4096)
            if len(data) < 20:
                continue
                
            client_ip = addr[0]
            devices = load_devices()
            
            if client_ip not in devices:
                print(f"[-] ELUTASÍTVA - Ismeretlen eszköz IP: {client_ip}")
                log_event(client_ip, "UNKNOWN_DEVICE", "REJECT")
                continue
                
            device_info = devices[client_ip]
            secret_bytes = device_info["secret"]
            hostname = device_info["hostname"]
            
            # RADIUS fejléc mezők kinyerése nyersen
            packet_type = data[0]
            packet_id = data[1]
            authenticator = data[4:20]
            
            # Attribútumok feldolgozása
            username = ""
            enc_password = b""
            
            offset = 20
            while offset < len(data):
                attr_type = data[offset]
                attr_len = data[offset+1]
                attr_val = data[offset+2:offset+attr_len]
                
                if attr_type == 1: # User-Name
                    username = attr_val.decode('utf-8', errors='ignore')
                elif attr_type == 2: # User-Password
                    enc_password = attr_val
                    
                offset += attr_len
                
            username = clean_strict(username)
            
            # Jelszó visszafejtése MD5 xor-ral
            password = ""
            if enc_password:
                hash_input = secret_bytes + authenticator
                md5_hash = hashlib.md5(hash_input).digest()
                decrypted = bytearray()
                for i in range(len(enc_password)):
                    decrypted.append(enc_password[i] ^ md5_hash[i % 16])
                password = clean_strict(decrypted.decode('utf-8', errors='ignore'))
            
            users = load_users()
            if username in users and users[username] == password:
                reply_code = 2 # Access-Accept
                status = "ACCEPT"
                print(f"[+] SIKERES AAA BELÉPÉS -> Felhasználó: '{username}' | Eszköz: {hostname} ({client_ip})")
            else:
                reply_code = 3 # Access-Reject
                status = "REJECT"
                print(f"[-] ELUTASÍTOTT AAA BELÉPÉS -> Felhasználó: '{username}' | Eszköz: {hostname} ({client_ip})")
                
            log_event(client_ip, username if username else "UNKNOWN", status)
            
            # Válaszcsomag összeállítása (Natív módon)
            reply_packet = bytearray([reply_code, packet_id, 0, 20]) # Típus, ID, Hossz (20 bájt alapesetben)
            
            # Válasz hitelesítő (Response Authenticator) generálása: MD5(Code + ID + Length + RequestAttributes + Secret)
            response_auth_input = reply_packet[0:4] + authenticator + secret_bytes
            response_auth = hashlib.md5(response_auth_input).digest()
            reply_packet[4:20] = response_auth
            
            sock.sendto(reply_packet, addr)
            
        except Exception as e:
            print(f"[-] Hiba történt a kérés feldolgozásakor: {e}")

if __name__ == '__main__':
    run_server()
"""

client_code = """import socket
import os
import random
import hashlib

def test_client():
    server_ip = "127.0.0.1"
    secret_bytes = b"secret123"
    
    print("=== RADIUS SZERVER TESZTELŐ KLIENS (NATÍV VERZIÓ) ===")
    username = input("Adja meg a felhasználónevet [admin]: ").strip() or "admin"
    password = input("Adja meg a jelszót [Cisco123!]: ").strip() or "Cisco123!"
    
    packet_id = random.randint(0, 255)
    authenticator = bytes(random.getrandbits(8) for _ in range(16))
    
    # Felhasználónév attribútum (Type=1)
    uname_bytes = username.encode('utf-8')
    attr_uname = bytes([1, len(uname_bytes) + 2]) + uname_bytes
    
    # Jelszó attribútum kódolása és igazítása (Type=2)
    pass_buf = password.encode('utf-8')
    if len(pass_buf) % 16 != 0:
        pass_buf += b'\\x00' * (16 - (len(pass_buf) % 16))
        
    hash_input = secret_bytes + authenticator
    md5_hash = hashlib.md5(hash_input).digest()
    
    enc_password = bytearray()
    for i in range(len(pass_buf)):
        enc_password.append(pass_buf[i] ^ md5_hash[i % 16])
    attr_pass = bytes([2, len(enc_password) + 2]) + bytes(enc_password)
    
    # Teljes csomag összeállítása
    attributes = attr_uname + attr_pass
    packet_length = 20 + len(attributes)
    
    header = bytearray([1, packet_id, (packet_length >> 8) & 0xff, packet_length & 0xff])
    packet = header + authenticator + attributes
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3.0)
    
    print(f"\\n[*] Kérés küldése -> {server_ip}:1812...")
    try:
        sock.sendto(packet, (server_ip, 1812))
        data, addr = sock.recvfrom(4096)
        
        reply_code = data[0]
        if reply_code == 2:
            print("[+] >>> SIKERES: ACCESS-ACCEPT <<< (A belépés engedélyezve!)")
        elif reply_code == 3:
            print("[-] >>> SIKERTELEN: ACCESS-REJECT <<< (A belépés elutasítva!)")
        else:
            print(f"[?] Ismeretlen válaszkód: {reply_code}")
            
    except socket.timeout:
        print(f"[-] Nem érkezett válasz a RADIUS szervertől (Időtúllépés).")
    except Exception as e:
        print(f"[-] Hiba történt: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    test_client()
"""

with open("server.py", "w", encoding="utf-8") as f: f.write(server_code)
with open("client.py", "w", encoding="utf-8") as f: f.write(client_code)
with open("devices.txt", "w", encoding="utf-8") as f: f.write("127.0.0.1;secret123;LocalHost_Switch")
with open("users.txt", "w", encoding="utf-8") as f: f.write("admin;Cisco123!")

print("[+] SIKER! Minden fájl lefrissítve a legbiztosabb, natív változatra.")
