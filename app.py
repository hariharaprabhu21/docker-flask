import os
from flask import request

# 1. Hardcoded secret
SECRET_KEY = "super_secret_hardcoded_password_123"

@app.route("/ping")
def ping():
    host = request.args.get("host")
    # 2. Command injection — user input passed straight to the shell
    os.system("ping -c 1 " + host)
    return "pinged"
