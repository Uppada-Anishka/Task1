# secure-text-cryptography-app

A beginner-friendly web application built with Python to demonstrate secure symmetric encryption and decryption. This app uses AES (Advanced Encryption Standard) to transform plaintext into ciphertext and back again.To ensure identical inputs yield completely unique outputs—mitigating the risk of frequency and dictionary attacks—the application implements a random Initialization Vector (IV) and a cryptographically secure salt.It relies on PBKDF2 (Password-Based Key Derivation Function 2) to securely generate the encryption key from a user-supplied password.

Key Features:
Unique Ciphertexts: Generates a fresh, random salt and IV for every encryption operation.
Symmetric AES Encryption: Secures text using industry-standard AES block ciphers.
Clean UI/API: Easily adaptable to a simple HTML/JS frontend or tested via FastAPI/Flask endpoints.

Prerequisites:
dependencies: pip install cryptography
Run the application script: python app.py
