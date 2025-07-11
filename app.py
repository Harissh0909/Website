from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload")
def upload_redirect():
    status_id = request.args.get("status_id")
    billcode = "ealcq5p7"  # Your ToyyibPay billcode

    if status_id != "1":
        return "❌ Payment failed or was cancelled."

    # Verify payment using ToyyibPay API
    response = requests.get(f"https://toyyibpay.com/index.php/api/getBillTransactions?billCode={billcode}")
    data = response.json()

    if not data or data[0]["billpaymentStatus"] != "1":
        return "❌ Payment verification failed."

    email = data[0]["payerEmail"]
    return render_template("upload.html", email=email)

@app.route("/upload", methods=["POST"])
def handle_upload():
    file = request.files["file"]
    email = request.form["email"]

    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    return f"✅ File '{filename}' uploaded successfully. Report will be sent to {email} soon."

if __name__ == "__main__":
    app.run(debug=True)
