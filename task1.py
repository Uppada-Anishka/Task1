import os
from flask import Flask, render_template, request, jsonify
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

app = Flask(__name__)

# Key Derivation Function (KDF) to make the password secure
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    password = data['password']
    plaintext = data['text'].encode()

    # Generate random Salt (16 bytes) and IV (12 bytes for GCM)
    salt = os.urandom(16)
    nonce = os.urandom(12) 

    key = derive_key(password, salt)
    
    # Encrypt
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    # Return the combined result, keeping the salt and nonce attached
    return jsonify({
        'encrypted_data': (salt + nonce + ciphertext).hex()
    })

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    password = data['password']
    
    # Convert hex back to bytes
    encrypted_bytes = bytes.fromhex(data['text'])

    # Parse out the salt, nonce, and ciphertext
    salt = encrypted_bytes[:16]
    nonce = encrypted_bytes[16:28]
    ciphertext = encrypted_bytes[28:]

    key = derive_key(password, salt)

    try:
        aesgcm = AESGCM(key)
        decrypted_text = aesgcm.decrypt(nonce, ciphertext, None).decode()
        return jsonify({'decrypted_text': decrypted_text})
    except Exception:
        return jsonify({'error': 'Decryption failed. Incorrect password or corrupted data.'}), 400

if __name__ == '__main__':
    app.run(debug=True)