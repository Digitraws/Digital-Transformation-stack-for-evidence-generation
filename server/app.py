from flask import Flask, render_template, url_for, request
import requests
import hashlib
from urllib.parse import urljoin
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import datetime

app = Flask(__name__)

# # Generate private and public keys at the beginning of the application
# PRIVATE_KEY = rsa.generate_private_key(
#     public_exponent=65537, key_size=512, backend=default_backend()
# )
# PUBLIC_KEY = PRIVATE_KEY.public_key()


# # Serialize the keys to PEM format
# PRIVATE_KEY_PEM = PRIVATE_KEY.private_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PrivateFormat.PKCS8,
#     encryption_algorithm=serialization.NoEncryption(),
# )
# PUBLIC_KEY_PEM = PUBLIC_KEY.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo,
# )

PRIVATE_KEY_PEM = b"-----BEGIN PRIVATE KEY-----\nMIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAwj2g1tfeH8DadiDf\n562BsjRDb7nTtaoSYZGMKdsZAb0Vlm6mNksvl6r1WsD6BmTFBglcM82e9XBBGNlB\n+8Y5SwIDAQABAkBU0CQSq19J7iN1wRUDTDd9YGSxvCo9AG3WPH8/J3Pb1bhavsa/\nCwvVSSI+9qmDYqiyJWX8akF7tWqMPi5mlJGBAiEA+KWgj3b7Fz44+IDA1QAMkjOZ\nzYChUw5CUDekNdJYKsMCIQDH/B7gTaVzT09H/1njF44f4o5CUfsl2M3XGasKQip+\n2QIfXy8IR+NEO6GWLYscRm2+Yjlep0yWdTUALbUfJ3teRQIhAMcYBDEwe//BPF+k\nIvvHbpHlvdTewxaZsctsXXB4ENB5AiEA3iVxufj4okBsDjRud+Z0B0nXmqf+uswX\n2aOA2d+kekk=\n-----END PRIVATE KEY-----\n"
PUBLIC_KEY_PEM = b"-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMI9oNbX3h/A2nYg3+etgbI0Q2+507Wq\nEmGRjCnbGQG9FZZupjZLL5eq9VrA+gZkxQYJXDPNnvVwQRjZQfvGOUsCAwEAAQ==\n-----END PUBLIC KEY-----\n"
# print(PRIVATE_KEY_PEM, PUBLIC_KEY_PEM, sep="\n")
PRIVATE_KEY = serialization.load_pem_private_key(
    PRIVATE_KEY_PEM, None, backend=default_backend()
)


@app.route("/")
def index():
    # Renders the index.html template for the root route.
    return render_template("index.html")


@app.route("/publickey")
def get_public_key():
    # Returns the serialized public key in PEM format.
    return PUBLIC_KEY_PEM


@app.route("/evidence")
def get_evidence():
    """
    Retrieves content from a specified URL, signs it using the private key, and returns the signature as a hexadecimal string.
    """
    endpoint = request.args.get("endpoint")
    base_url = request.url_root.rstrip("/")

    try:
        url = urljoin(base_url, endpoint)
        print(url)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        content = response.content
        print(type(content))

        # Sign the content using the private key
        signature = PRIVATE_KEY.sign(
            content,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        print(signature)
        print("h", type(signature.hex()))
        return signature.hex()

    except Exception as e:
        return f"Error: {str(e)}"


@app.after_request
def add_signature_header(response):
    response.direct_passthrough = False

    timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    data = response.data
    content = str(timestamp).encode() + data

    print(hashlib.sha256(data).digest())

    signature = PRIVATE_KEY.sign(
        content,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), salt_length=0
        ),
        hashes.SHA256(),
    )
    print(len(signature.hex()))

    response.headers["X-Signature-timestamp"] = timestamp
    response.headers["X-Signature"] = signature.hex()
    # response.headers["X-Signature"] = "dead"
    return response


if __name__ == "__main__":
    app.run(debug=True)
