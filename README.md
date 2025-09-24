# UNL - Unlock N Load

**UNL** is an interactive Python tool to brute-force decrypt files encrypted with a key derived from a password and salt.  
It is designed as a companion to the LNL (Lock N Loaded) encryptor tool.

---

## Features

- Interactive terminal prompts for:
  - Encrypted folder path
  - Wordlist file path
  - Salt file path
- `ls` support to list files in the current directory
- Recursive decryption of all files in a folder
- Clean progress display showing password attempts and decrypted file counts
- Stops automatically when a password successfully decrypts any file

---

## Important

- **Salt is required**: UNL cannot decrypt files without the original salt used during encryption. Even with the correct password, decryption will fail if the salt is missing.
- Use this tool **only** on files you own or have explicit permission to decrypt. Unauthorized decryption attempts are illegal.

---

## Requirements

- Python 3.8+
- `cryptography` library

Install dependencies:

```bash
pip install cryptography
```

---

## Usage

Run the script in the terminal:

```bash
python3 unl.py
```

Follow the prompts:

1. Enter the path to the folder containing encrypted files.
2. Enter the path to the wordlist file.
3. Enter the path to the salt file.
4. Type `ls` to list the current directory contents if needed.

The script will attempt passwords from the wordlist to decrypt the files.

---

## Author

Andrea  
GitHub: [@andreakangethe](https://github.com/AndreaKangethe)
