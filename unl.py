import base64
import pathlib
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os

def display_banner():
    banner = """
██╗   ██╗███╗   ██╗██╗      ██████╗  ██████╗██╗  ██╗    ███╗   ██╗    ██╗      ██████╗  █████╗ ██████╗ 
██║   ██║████╗  ██║██║     ██╔═══██╗██╔════╝██║ ██╔╝    ████╗  ██║    ██║     ██╔═══██╗██╔══██╗██╔══██╗
██║   ██║██╔██╗ ██║██║     ██║   ██║██║     █████╔╝     ██╔██╗ ██║    ██║     ██║   ██║███████║██║  ██║
██║   ██║██║╚██╗██║██║     ██║   ██║██║     ██╔═██╗     ██║╚██╗██║    ██║     ██║   ██║██╔══██║██║  ██║
╚██████╔╝██║ ╚████║███████╗╚██████╔╝╚██████╗██║  ██╗    ██║ ╚████║    ███████╗╚██████╔╝██║  ██║██████╔╝
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝    ╚═╝  ╚═══╝    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 

                                   Unlock N Load (UNL)
                                        By: Andrea
                                   GitHub: @andreakangethe
    """
    print(banner)

def get_path(prompt):
    while True:
        path = input(prompt).strip()
        if path.lower() == "ls":
            for f in os.listdir():
                print(f)
            continue
        if not path:
            continue
        if pathlib.Path(path).exists():
            return path
        print("Invalid path. Try again or type 'ls' to list current directory.")

def derive_key(password, salt):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as f:
        encrypted_data = f.read()
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(file_path, "wb") as f:
            f.write(decrypted_data)
        return True
    except InvalidToken:
        return False

def main():
    display_banner()

    folder = get_path("Enter path to encrypted folder (or 'ls' to list): ")
    wordlist_file = get_path("Enter path to wordlist file (or 'ls' to list): ")
    salt_file = get_path("Enter path to salt file (or 'ls' to list): ")

    with open(salt_file, "rb") as f:
        salt = f.read()

    with open(wordlist_file, "r", encoding="utf-8") as f:
        passwords = [line.strip() for line in f]

    files = [f for f in pathlib.Path(folder).rglob("*") if f.is_file()]
    total_files = len(files)
    if total_files == 0:
        print("No files found in folder.")
        return

    print(f"\n[*] Starting brute-force on {total_files} files...\n")

    for pwd_index, pwd in enumerate(passwords, 1):
        key = derive_key(pwd, salt)
        decrypted_count = 0
        for file_index, file_path in enumerate(files, 1):
            if decrypt_file(file_path, key):
                decrypted_count += 1

        if decrypted_count > 0:
            print(f"[+] Password found: {pwd} → Decrypted {decrypted_count}/{total_files} files")
            break
        else:
            print(f"[{pwd_index}/{len(passwords)}] Tried password: {pwd}")
    else:
        print("[-] Password not found in wordlist.")

if __name__ == "__main__":
    main()
