import subprocess

import requests
import yaml
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello from a very insecure demo app! Do NOT use this in production."


@app.route("/ping", methods=["GET"])
def ping():
    """
    Extremely naive endpoint:
    - Takes a 'url' query parameter
    - Fetches that URL with requests
    - Returns the body directly

    It's easy for tools to flag this kind of pattern as risky (SSRF-style).
    """
    url = request.args.get("url", "https://example.com")
    resp = requests.get(url)
    return resp.text


@app.route("/run", methods=["POST"])
def run():
    """
    SUPER DANGEROUS on purpose:

    - Reads raw request body as YAML
    - Uses yaml.load (unsafe) on untrusted input
    - Reads a 'cmd' key from YAML
    - Runs that command with shell=True

    This is exactly the kind of thing security tools should scream about.
    """
    raw_body = request.data.decode("utf-8")

    # Intentionally unsafe usage of yaml.load on attacker-controlled input.
    # (Modern, safe code should use yaml.safe_load instead.)
    config = yaml.load(raw_body)

    cmd = config.get("cmd", "echo hello from insecure app")

    # Intentionally unsafe: shell=True AND user-controlled command.
    # This is a classic command injection sink.
    output = subprocess.check_output(cmd, shell=True, text=True)

    return f"Command output:\n{output}"


if __name__ == "__main__":
    # debug=True is also something tools can flag in some contexts
    app.run(host="0.0.0.0", port=5000, debug=True)
