from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import qrcode, io, os
from fpdf import FPDF
import sqlite3

app = Flask(__name__)
CORS(app)

# Database setup
def init_db():
    conn = sqlite3.connect("certificates.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS certificates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    course TEXT,
                    date TEXT
                )""")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "✅ Certificate Generator Backend is running!"

@app.route("/generate", methods=["POST"])
def generate_certificate():
    data = request.json
    name, course, date = data["name"], data["course"], data["date"]

    # Save to DB
    conn = sqlite3.connect("certificates.db")
    c = conn.cursor()
    c.execute("INSERT INTO certificates (name, course, date) VALUES (?, ?, ?)", (name, course, date))
    cert_id = c.lastrowid
    conn.commit()
    conn.close()

    # Generate QR code and save to file
    qr_path = f"qr_{cert_id}.png"
    qr = qrcode.make(f"http://localhost:5173/verify/{cert_id}")
    qr.save(qr_path)

    # Generate PDF with styled design
    pdf = FPDF("L", "mm", "A4")  # Landscape A4
    pdf.add_page()

    # Add border
    pdf.set_line_width(1)
    pdf.rect(10, 10, 277, 190)

    # Title
    pdf.set_font("Arial", "B", 28)
    pdf.set_text_color(0, 102, 204)  # Blue
    pdf.cell(0, 30, "Certificate of Completion", ln=True, align="C")

    # Subtitle
    pdf.set_font("Arial", "I", 18)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 15, "This certificate is proudly presented to", ln=True, align="C")

    # Recipient Name
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 20, name, ln=True, align="C")

    # Course & Date
    pdf.set_font("Arial", "", 16)
    pdf.cell(0, 15, f"For successfully completing {course}", ln=True, align="C")
    pdf.cell(0, 15, f"Date: {date}", ln=True, align="C")

    # QR Code
    pdf.image(qr_path, x=120, y=120, w=50, h=50)

    # Signature line
    pdf.set_font("Arial", "I", 14)
    pdf.cell(0, 40, "Authorized Signature", ln=True, align="R")

    # Convert PDF to bytes
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    pdf_io = io.BytesIO(pdf_bytes)

    # Cleanup QR file
    os.remove(qr_path)

    return send_file(pdf_io, as_attachment=True, download_name="certificate.pdf", mimetype="application/pdf")

@app.route("/verify/<int:cert_id>")
def verify_certificate(cert_id):
    conn = sqlite3.connect("certificates.db")
    c = conn.cursor()
    c.execute("SELECT * FROM certificates WHERE id=?", (cert_id,))
    cert = c.fetchone()
    conn.close()

    if cert:
        return jsonify({"id": cert[0], "name": cert[1], "course": cert[2], "date": cert[3]})
    else:
        return jsonify({"error": "Certificate not found"}), 404

if __name__ == "__main__":
    init_db()
    print(">>> Starting Certificate Generator Backend...")
    app.run(host="127.0.0.1", port=5000, debug=True)