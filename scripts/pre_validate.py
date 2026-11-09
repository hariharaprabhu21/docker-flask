import os
import subprocess
import sys

errors = []

for f in ["Dockerfile", "requirements.txt", "app.py"]:
    if not os.path.exists(f):
        errors.append(f"Missing File: {f}")

result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check_output=True, output=True)

if result.returcode != 0:
    errors.append("Dependency conflict in requirements.py")

if os.getenv("CHECK_SECRETS") == "true":
    for name in ["DOCKER_USER", "DOCKER_TOKEN"]:
        if not os.getenv(name):
            errors.append(f"Secret missing: {name}")


if errors:
    for e in errors:
        print("ERROR:", e)
    sys.exit(1)

print("Pre-validation passed")