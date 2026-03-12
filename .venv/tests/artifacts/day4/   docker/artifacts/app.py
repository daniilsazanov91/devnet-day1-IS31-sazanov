from flask import Flask
import hashlib
import os

app = Flask(__name__)

token = os.getenv("STUDENT_TOKEN", "none")
token_hash8 = hashlib.sha256(token.encode()).hexdigest()[:8]

@app.route("/")
def home():
    return f"""
    <h1>Sample Docker App</h1>
    TOKEN_HASH8={token_hash8}
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
