import base64
import time
from cryptography.hazmat.primitives.asymmetric import rsa

keys = []

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    kid = f"key-{int(time.time())}"
    expiry = time.time() + 3600 # 1 hour expiry
    return {
        "kid": kid,
        "private_key": private_key,
        "public_key": public_key,
        "expiry": expiry
    }

def to_base64_url(value):
    return base64.urlsafe_b64encode(value).decode('utf-8').rstrip("=")

def get_public_keys():
    valid_keys = [
        {
            "kid": key['kid'],
            "kty": "RSA",
            "n": to_base64_url(key['public_key'].public_numbers().n.to_bytes(256, 'big')),
            "e": to_base64_url(key['public_key'].public_numbers().e.to_bytes(3, 'big'))
        } for key in keys if key['expiry'] > time.time()
    ]
    return {"keys": valid_keys}