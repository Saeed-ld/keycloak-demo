from flask import Flask, jsonify, request
import jwt
import requests
from functools import wraps

app = Flask(__name__)

KEYCLOAK_URL = "http://localhost:8080"
REALM = "access-lab"
ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"

# Download Keycloak's public signing keys
jwks_client = jwt.PyJWKClient(
    f"{ISSUER}/protocol/openid-connect/certs"
)


def require_role(required_role):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get("Authorization", "")

            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing bearer token"}), 401

            token = auth_header.split(" ", 1)[1]

            try:
                signing_key = jwks_client.get_signing_key_from_jwt(token)

                claims = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=["RS256"],
                    issuer=ISSUER,
                    options={"verify_aud": False}
                )

            except jwt.PyJWTError:
                return jsonify({"error": "Invalid or expired token"}), 401

            roles = claims.get("realm_access", {}).get("roles", [])

            if required_role not in roles:
                return jsonify({
                    "error": "Access denied",
                    "required_role": required_role
                }), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/")
def home():
    return jsonify({
        "application": "Keycloak Role-Based Access Demo",
        "endpoints": ["/engineering", "/finance"]
    })


@app.route("/engineering")
@require_role("engineering-access")
def engineering():
    return jsonify({"message": "Welcome to Engineering!"})


@app.route("/finance")
@require_role("finance-access")
def finance():
    return jsonify({"message": "Welcome to Finance!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)
