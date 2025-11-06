from flask import Flask, request, render_template
import requests
from datetime import datetime

app = Flask(__name__)

ITEXMO_API_URL = "https://www.itexmo.com/php_api/api.php"
API_CODE = "PR-JOYNA703440_PYO4M"

def send_sms(recipient, message):
    payload = {
        '1': recipient,
        '2': message,
        '3': API_CODE
    }
    try:
        response = requests.post(ITEXMO_API_URL, data=payload, timeout=10)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    status = ""
    if request.method == "POST":
        student = request.form["student"]
        number = request.form["number"]
        formatted = "+63" + number[1:] if number.startswith("0") else number
        message = f"Hello! Your child, {student}, was marked absent today ({datetime.now().strftime('%b %d, %Y')}). - Dr. Rene Arduo"
        response = send_sms(formatted, message)
        status = f"Response: {response}"
    return render_template("index.html", status=status)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

