
from flask import Flask, request, jsonify
import os, time, hmac, base64, struct, hashlib, jwt

app = Flask(__name__)
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret_here")
MFA_SECRET = os.getenv("MFA_SECRET_SEED", "JBSWY3DPEHPK3PXP")

def totp_now(secret, interval=30):
    key = base64.b32decode(secret, casefold=True)
    t = int(time.time() // interval)
    msg = struct.pack(">Q", t)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    token = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return f"{token:06d}"

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username:
        return jsonify({"error":"missing username"}), 400
    tmp = jwt.encode({"user": username, "stage": "mfa_pending"}, JWT_SECRET, algorithm="HS256")
    return jsonify({"tmp_token": tmp})

@app.route('/auth/mfa/verify', methods=['POST'])
def verify():
    data = request.get_json() or {}
    tmp = data.get("tmp_token")
    code = data.get("code")
    if not tmp or not code:
        return jsonify({"error":"missing"}), 400
    try:
        payload = jwt.decode(tmp, JWT_SECRET, algorithms=["HS256"])
    except Exception as e:
        return jsonify({"error":"invalid token", "details": str(e)}), 400
    expected = totp_now(MFA_SECRET)
    if str(code) == expected:
        token = jwt.encode({"user": payload.get("user")}, JWT_SECRET, algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"error":"invalid code"}), 401

@app.route('/auth/validate', methods=['GET'])
def validate():
    auth = request.headers.get("Authorization","").replace("Bearer ","").strip()
    if not auth:
        return jsonify({"valid": False}), 401
    try:
        jwt.decode(auth, JWT_SECRET, algorithms=["HS256"])
        return jsonify({"valid": True})
    except:
        return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6200)
