import requests
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend

def verify(signature, content, public_key):
    # Calculate the SHA-1 hash of the content
    content_hash = hashlib.sha1(content).digest()

    # Verify the signature using the provided public key
    public_key_obj = load_pem_public_key(public_key, backend=default_backend())
    try:
        public_key_obj.verify(
            signature,
            content_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

def main():
    # Replace 'http://yourdomain.com' with the actual base URL of your Flask app
    base_url = 'http://localhost:5000'

    # Get the public key from the server
    response = requests.get(f"{base_url}/publickey")
    pub_key_pem = response.text.encode('utf-8')

    # Get the content from the server
    response = requests.get(f"{base_url}/")
    content = response.content

    # Get the signature from the server
    response = requests.get(f"{base_url}/evidence?=endpoint=/")
    signature = response.content
    print(content, signature)

    # Verify the signature with the public key
    result = verify(signature, content, pub_key_pem)

    print(result)

if __name__ == '__main__':
    main()
