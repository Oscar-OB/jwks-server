from flask import Flask, jsonify, request, make_response
from urllib.parse import urlparse, parse_qs
import datetime
import jwt

from keys import key_manager

app = Flask(__name__)


# Endpoint for generating JWT token
@app.route('/auth', methods=['POST'])
def auth():
    # Parse query parameters
    parsed_path = urlparse(request.url)
    params = parse_qs(parsed_path.query)

    headers = {
        "kid": "goodKID"
    }
    token_payload = {
        "user": "username",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
    }

    # Check for 'expired' in params to generate an expired token
    if 'expired' in params:
        headers["kid"] = "expiredKID"
        token_payload["exp"] = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)

    # Encode the JWT
    encoded_jwt = jwt.encode(token_payload, key_manager.pem, algorithm='RS256', headers=headers)

    # Return the encoded JWT as a response
    return make_response(encoded_jwt, 200)


# Endpoint for JWKS
@app.route('/.well-known/jwks.json', methods=['GET'])
def get_jwks():
    keys = {
        "keys": [
            {
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "kid": "goodKID",
                "n": key_manager.to_base_64(key_manager.numbers.public_numbers.n),
                "e": key_manager.to_base_64(key_manager.numbers.public_numbers.e),
            }
        ]
    }

    # Return the JWKS as JSON response
    return jsonify(keys)


# Error handler for unsupported methods
@app.errorhandler(405)
def method_not_allowed(e):
    return make_response(jsonify(error="Method not allowed"), 405)


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
