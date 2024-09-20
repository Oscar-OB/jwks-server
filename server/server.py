from flask import Flask, jsonify, request
import time
import jwt
from keys.key_manager import generate_rsa_keypair, get_public_keys, keys

app = Flask(__name__)


@app.route('/jwks', methods=['GET'])
def jwks():

    public_keys = get_public_keys()
    return jsonify(public_keys)


@app.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired')
    current_time = time.time()

    # Use an expired key if requested
    key_pair = next((k for k in keys if expired and k['expiry'] < current_time), None)
    if not key_pair:
        key_pair = next((k for k in keys if k['expiry'] > current_time), None)

    if not key_pair:
        return jsonify({"error": "No valid key pair available"}), 400

    # Create a JWT
    payload = {"sub": "user", "iat": current_time}
    token = jwt.encode(payload, key_pair['private_key'], algorithm='RS256')

    return jsonify({"token": token})


if __name__ == '__main__':
    # Generate keys at startup
    key_pair = generate_rsa_keypair()
    keys.append(key_pair)
    #print("Generated keys:", keys)
    #keys.append(generate_rsa_keypair())
    app.run(host='0.0.0.0', port=8080)